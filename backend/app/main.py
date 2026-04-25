"""
Main script demonstrating how to use the enhanced EDA system with explainability features.
This integrates: Enhanced EDA, Charts, Prompts, Explainability, and Gemini API calls.
"""

import pandas as pd
from app.eda_engine import analyze
from app.charts import generate_charts
from app.prompt_builder import build_structured_prompt, build_simple_explanation_prompt
from app.chart_explainability_complete import (
    generate_chart_explanations,
    generate_summary_explanation,
    generate_chart_interpretation_guide
)
from app.gemini_client import call_gemini
import json


def run_complete_eda_with_explainability(csv_file_path: str, output_dir: str = './results') -> dict:
    """
    Run complete EDA pipeline with AI-powered explanations for all outputs.
    
    Args:
        csv_file_path: Path to CSV file
        output_dir: Directory to save outputs
    
    Returns:
        Dictionary containing all results and explanations
    """
    
    print("=" * 80)
    print("INSIGHT-FORGE: ENHANCED EDA WITH EXPLAINABILITY")
    print("=" * 80)
    
    # ============ STEP 1: LOAD DATA ============
    print("\n[STEP 1] Loading data...")
    try:
        df = pd.read_csv(csv_file_path)
        print(f"✓ Loaded {df.shape[0]} rows × {df.shape[1]} columns")
    except Exception as e:
        print(f"✗ Error loading file: {e}")
        return {}
    
    # ============ STEP 2: RUN ENHANCED EDA ============
    print("\n[STEP 2] Running comprehensive exploratory data analysis...")
    try:
        eda_stats = analyze(df)
        print(f"✓ EDA complete!")
        print(f"  - Data Quality Score: {eda_stats['data_quality_score']['overall_score']}/100")
        print(f"  - Missing Data: {eda_stats['missing_data_summary']['missing_percentage']}%")
        print(f"  - Outliers Found: {eda_stats['total_outliers']}")
    except Exception as e:
        print(f"✗ Error in EDA analysis: {e}")
        return {}
    
    # ============ STEP 3: GENERATE CHARTS ============
    print("\n[STEP 3] Generating visualizations...")
    try:
        chart_data = generate_charts(df)
        print(f"✓ Generated {len(chart_data['distributions'])} distribution histograms")
        print(f"✓ Generated {len(chart_data['kde_plots'])} KDE density plots")
        print(f"✓ Generated {len(chart_data['scatter_plots'])} scatter / relationship plots")
        print(f"✓ Generated {len(chart_data['line_charts'])} line / trend charts")
        print(f"✓ Generated {len(chart_data['categorical_distributions'])} categorical bar charts")
        print(f"✓ Generated {len(chart_data['boxplots'])} box plots")
        print(f"✓ Generated {len(chart_data['violin_plots'])} violin plots")
        if chart_data['correlation']:
            print(f"✓ Generated correlation heatmap")
        if chart_data['pair_plot']:
            print(f"✓ Generated multi-variable pair plot")
        print(f"✓ Generated {len(chart_data['bubble_charts'])} bubble charts")
        print(f"✓ Generated {len(chart_data['pie_charts'])} pie / donut charts")
        if chart_data['missing_data_heatmap']:
            print(f"✓ Generated missing data visualization")
        if chart_data['numeric_summary_stats']:
            print(f"✓ Generated numeric summary stats dashboard")
    except Exception as e:
        print(f"✗ Error generating charts: {e}")
        chart_data = {}
    
    # ============ STEP 4: GENERATE CHART EXPLANATIONS ============
    print("\n[STEP 4] Generating AI-powered chart explanations (plain language)...")
    try:
        chart_explanations = generate_chart_explanations(eda_stats, chart_data)
        print(f"✓ Generated explanations for {len(chart_explanations)} charts")
        
        # Also generate interpretation guide
        interpretation_guide = generate_chart_interpretation_guide()
        print(f"✓ Generated beginner's guide for all 13 chart types")
    except Exception as e:
        print(f"⚠ Error generating chart explanations: {e}")
        chart_explanations = {}
        interpretation_guide = {}
    
    # ============ STEP 5: GENERATE SUMMARY EXPLANATION ============
    print("\n[STEP 5] Generating dataset summary in plain language...")
    try:
        summary_explanation = generate_summary_explanation(eda_stats)
        print(f"✓ Generated dataset summary explanation")
    except Exception as e:
        print(f"⚠ Error generating summary: {e}")
        summary_explanation = "Dataset analysis complete."
    
    # ============ STEP 6: BUILD STRUCTURED PROMPT FOR INSIGHTS ============
    print("\n[STEP 6] Building AI prompt for comprehensive analysis...")
    try:
        structured_prompt = build_structured_prompt(eda_stats)
        print(f"✓ Prompt built ({len(structured_prompt)} characters)")
    except Exception as e:
        print(f"✗ Error building prompt: {e}")
        structured_prompt = ""
    
    # ============ STEP 7: CALL GEMINI FOR DETAILED INSIGHTS ============
    print("\n[STEP 7] Calling Gemini AI for detailed analysis...")
    print("(This may take a moment...)")
    try:
        gemini_insights = call_gemini(structured_prompt)
        print(f"✓ Received comprehensive analysis from Gemini")
    except Exception as e:
        print(f"✗ Error calling Gemini: {e}")
        gemini_insights = {}
    
    # ============ STEP 8: SIMPLIFY INSIGHTS FOR NON-TECHNICAL USERS ============
    print("\n[STEP 8] Simplifying insights for non-technical stakeholders...")
    try:
        simplification_prompt = build_simple_explanation_prompt(gemini_insights)
        simplified_insights = call_gemini(simplification_prompt)
        print(f"✓ Generated simplified explanations")
    except Exception as e:
        print(f"⚠ Error simplifying insights: {e}")
        simplified_insights = {}
    
    # ============ STEP 9: COMPILE RESULTS ============
    print("\n[STEP 9] Compiling final results...")
    
    final_results = {
        'dataset_info': {
            'filename': csv_file_path,
            'shape': eda_stats['shape'],
            'data_quality_score': eda_stats['data_quality_score'],
            'columns': eda_stats['column_names']
        },
        
        'eda_statistics': eda_stats,
        
        'visualizations': chart_data,
        
        'explanations': {
            'chart_explanations': chart_explanations,
            'interpretation_guide': interpretation_guide,
            'dataset_summary': summary_explanation
        },
        
        'gemini_analysis': {
            'detailed_insights': gemini_insights,
            'simplified_for_non_technical': simplified_insights
        },
        
        'quality_metrics': {
            'data_quality': eda_stats['data_quality_score'],
            'missing_data': eda_stats['missing_data_summary'],
            'outliers': eda_stats['total_outliers']
        }
    }
    
    print(f"✓ Results compiled successfully!")
    
    # ============ STEP 10: SAVE RESULTS ============
    print("\n[STEP 10] Saving results...")
    try:
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Save JSON results (strip base64 images — too large for JSON)
        image_keys = ['distributions', 'kde_plots', 'scatter_plots', 'line_charts',
                      'boxplots', 'violin_plots', 'bubble_charts', 'pie_charts',
                      'categorical_distributions']
        results_without_images = final_results.copy()
        results_without_images['visualizations'] = {
            k: v for k, v in chart_data.items() if k not in image_keys
        }
        with open(f'{output_dir}/eda_results.json', 'w') as f:
            json.dump(results_without_images, f, indent=2, default=str)
        print(f"✓ Saved EDA results to {output_dir}/eda_results.json")
        
        # Save comprehensive text report
        report_content = generate_text_report(final_results)
        with open(f'{output_dir}/eda_report.txt', 'w') as f:
            f.write(report_content)
        print(f"✓ Saved comprehensive report to {output_dir}/eda_report.txt")
        
    except Exception as e:
        print(f"⚠ Error saving results: {e}")
    
    print("\n" + "=" * 80)
    print("EDA ANALYSIS COMPLETE ✓")
    print("=" * 80)
    
    return final_results


def generate_text_report(results: dict) -> str:
    """
    Generate a comprehensive text report from results.
    
    Args:
        results: Dictionary containing all analysis results
    
    Returns:
        Formatted text report
    """
    
    report = """
================================================================================
                    INSIGHT-FORGE EDA ANALYSIS REPORT
================================================================================

1. DATASET OVERVIEW
───────────────────────────────────────────────────────────────────────────────
"""
    
    info    = results.get('dataset_info', {})
    quality = results.get('quality_metrics', {})
    
    report += f"""
File: {info.get('filename')}
Shape: {info.get('shape', {}).get('rows')} rows × {info.get('shape', {}).get('columns')} columns
Data Quality Score: {quality.get('data_quality', {}).get('overall_score')}/100

2. DATA QUALITY ASSESSMENT
───────────────────────────────────────────────────────────────────────────────
"""
    
    missing = quality.get('missing_data', {})
    report += f"""
Missing Data: {missing.get('missing_percentage')}% ({missing.get('total_missing')} cells)
Outliers Detected: {quality.get('outliers')}
Data Completeness: {quality.get('data_quality', {}).get('completeness_score')}/100

3. PLAIN LANGUAGE EXPLANATION
───────────────────────────────────────────────────────────────────────────────
"""
    
    explanations = results.get('explanations', {})
    report += f"\n{explanations.get('dataset_summary', 'Summary unavailable')}\n"
    
    report += """
4. KEY INSIGHTS FROM AI ANALYSIS
───────────────────────────────────────────────────────────────────────────────
"""
    
    insights = results.get('gemini_analysis', {}).get('detailed_insights', {})
    
    if insights:
        if 'executive_summary' in insights:
            report += f"\nEXECUTIVE SUMMARY:\n{insights.get('executive_summary', 'N/A')}\n"
        
        if 'key_trends' in insights:
            report += f"\nKEY TRENDS:\n"
            for trend in insights.get('key_trends', []):
                report += f"  • {trend}\n"
        
        if 'actionable_business_insights' in insights:
            report += f"\nBUSINESS INSIGHTS:\n"
            for insight in insights.get('actionable_business_insights', []):
                report += f"  • {insight}\n"
        
        if 'next_steps_and_recommendations' in insights:
            next_steps = insights.get('next_steps_and_recommendations', {})
            report += f"\nRECOMMENDED NEXT STEPS:\n"
            for action in next_steps.get('immediate_actions', []):
                report += f"  • {action}\n"
    
    report += """
5. CHART INTERPRETATION GUIDE
───────────────────────────────────────────────────────────────────────────────
"""
    
    guide = explanations.get('interpretation_guide', {})
    for chart_type, explanation in guide.items():
        report += f"\n{chart_type.upper()}:\n{explanation}\n"
    
    report += """
================================================================================
                           END OF REPORT
================================================================================
Generated by Insight-Forge EDA System
For questions about the analysis, see the detailed JSON results file.
"""
    
    return report

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import tempfile
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Insight-Forge Backend Running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        # 👉 your SAME function
        results = run_complete_eda_with_explainability(tmp_path)

        os.remove(tmp_path)

        return {
            "message": "Success",
            "results": results
        }

    except Exception as e:
        return {"error": str(e)}