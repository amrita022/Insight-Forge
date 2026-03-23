from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import io
import json
import traceback
from typing import Optional

from app.eda_engine import analyze
from app.prompt_builder import build_structured_prompt, build_baseline_prompt
from app.gemini_client import call_gemini
from app.charts import generate_charts

app = FastAPI(title="Insight Forge API", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
<<<<<<< HEAD
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
=======
    allow_origins=["*"],
>>>>>>> 1db73968ad37f13925329a7797a4f57efc5e4f69
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
        
        # Generate charts
        charts = generate_charts(df)
        
        # Build structured prompt and get Gemini insights
        prompt = build_structured_prompt(stats)
        gemini_response = call_gemini(prompt)
        
        # Combine results
        result = {
            "status": "success",
            "stats": stats,
            "charts": charts,
            "insights": gemini_response,
        }
        
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except pd.errors.ParserError as e:
        raise HTTPException(status_code=400, detail=f"Invalid CSV format: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze/baseline")
async def analyze_baseline(file: UploadFile = File(...)):
    """
    Baseline endpoint for comparison.
    Sends raw sample rows to Gemini with minimal prompt.
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
        
        # Build baseline prompt with raw sample
        prompt = build_baseline_prompt(df)
        
        # Get Gemini insights
        gemini_response = call_gemini(prompt)
        
        # Generate charts for baseline as well
        charts = generate_charts(df)
        
        result = {
            "status": "success",
            "charts": charts,
            "insights": gemini_response,
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
