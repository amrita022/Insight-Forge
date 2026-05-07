from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import io
import json
import traceback
from typing import Optional

from app.eda_engine import analyze, explain_pairwise_relations, explain_outliers, explain_distributions, explain_correlation_matrix
from app.prompt_builder import build_structured_prompt, build_baseline_prompt
from app.gemini_client import call_gemini
from app.charts import generate_charts
from app.image_explain import extract_text_from_image_bytes, build_image_details, explain_from_ocr, get_supported_chart_types
from app.prompt_builder import build_image_prompt

app = FastAPI(title="Insight Forge API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
async def analyze_csv(file: UploadFile = File(...)):
    """
    Full EDA pipeline endpoint.
    Accepts CSV file, runs complete analysis with Gemini insights.
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV file")
        
        # Read CSV into DataFrame
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        if df.empty:
            raise HTTPException(status_code=400, detail="CSV file is empty")
        
        # Run EDA analysis
        stats = analyze(df)
        # Add automated pairwise explanations for top correlated pairs
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        stats['pair_explanations'] = explain_pairwise_relations(df, numeric_cols)
        stats['outlier_explanations'] = explain_outliers(df, numeric_cols)
        stats['distribution_explanations'] = explain_distributions(df, numeric_cols)
        stats['correlation_explanation'] = explain_correlation_matrix(df, numeric_cols)
        
        # Generate charts
        charts = generate_charts(df)
        
        # Build structured prompt and get Gemini insights (optional)
        gemini_response = None
        gemini_error = None
        try:
            prompt = build_structured_prompt(stats)
            gemini_response = call_gemini(prompt)
        except Exception as llm_err:
            gemini_error = f"LLM insights unavailable: {str(llm_err)}"
            # Continue without LLM insights
        
        # Combine results
        result = {
            "status": "success",
            "stats": stats,
            "charts": charts,
            "insights": gemini_response or {"note": gemini_error or "LLM insights not available"},
        }
        
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except pd.errors.ParserError as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/explain/image")
async def explain_image(file: UploadFile = File(...)):
    """Explain an uploaded chart image in depth using OCR + Gemini analysis.
    Accepts common image formats. Returns detailed structured JSON explanation.
    """
    try:
        if not any(file.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']):
            raise HTTPException(status_code=400, detail="File must be an image (png/jpg/bmp/gif)")

        contents = await file.read()
        extracted = extract_text_from_image_bytes(contents)
        details = build_image_details(extracted)

        # Generate deterministic explanation (always available)
        fallback = None
        try:
            fallback = explain_from_ocr(extracted)
        except Exception:
            fallback = None

        # Try to get LLM explanation (optional)
        model_text = None
        llm_error = None
        try:
            prompt = build_image_prompt(extracted, details)
            gemini_raw = call_gemini(prompt, parse_json=False)
            model_text = gemini_raw.get('text')
        except Exception as llm_err:
            llm_error = f"Model explanation unavailable: {str(llm_err)}"

        return JSONResponse(content={
            'status': 'success',
            'extracted_text': extracted,
            'details': details,
            'model_text': model_text or llm_error or None,
            'fallback_explanation': fallback,
            'detected_chart_type': details.get('detected_chart_type', 'unknown_chart'),
            'supported_uploads': get_supported_chart_types()
        })

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/baseline")
async def analyze_baseline(file: UploadFile = File(...)):
    """
    Baseline endpoint for comparison.
    Sends only a lightweight sample-based prompt to Gemini.
    """
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV file")
        
        # Read CSV into DataFrame
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        if df.empty:
            raise HTTPException(status_code=400, detail="CSV file is empty")
        
        # Generate charts for baseline as well
        charts = generate_charts(df)
        
        # Build baseline prompt with raw sample (optional LLM)
        gemini_response = None
        gemini_error = None
        try:
            prompt = build_baseline_prompt(df)
            gemini_response = call_gemini(prompt)
        except Exception as llm_err:
            gemini_error = f"LLM insights unavailable: {str(llm_err)}"
        
        result = {
            "status": "success",
            "charts": charts,
            "analysis_mode": "baseline",
            "comparison_note": "Baseline analysis is a quick preview: it uses only the first rows of the file and a short sample-based prompt, without the deeper statistical breakdown used in structured analysis.",
            "insights": gemini_response or {"note": gemini_error or "LLM insights not available"},
        }
        
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except pd.errors.ParserError as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return JSONResponse(content={"status": "healthy"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
