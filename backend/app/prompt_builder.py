import pandas as pd
from typing import Dict, Any
import json


def build_structured_prompt(stats: Dict[str, Any]) -> str:
    """
    Build a detailed, structured prompt for Gemini from EDA stats.
    
    Args:
        stats: Dictionary from eda_engine.analyze()
    
    Returns:
        Detailed prompt string instructing Gemini to return JSON
    """
    # If pair explanations exist, include them
    pair_explanations = stats.get('pair_explanations') if isinstance(stats, dict) else None

    prompt = f"""You are an expert data analyst. Analyze the following dataset statistics and provide insights.

DATASET OVERVIEW:
- Shape: {stats['shape']['rows']} rows × {stats['shape']['columns']} columns
- Columns: {', '.join(stats['column_names'])}
- Data Types: {json.dumps(stats['dtypes'], indent=2)}

MISSING VALUES:
{json.dumps(stats['missing_values'], indent=2)}

DESCRIPTIVE STATISTICS (Numeric Columns):
{json.dumps(stats['descriptive_stats'], indent=2)}

CORRELATION MATRIX:
{json.dumps(stats['correlation_matrix'], indent=2) if stats['correlation_matrix'] else 'Not available (insufficient numeric columns)'}

PAIRWISE EXPLANATIONS (automated):
{json.dumps(pair_explanations, indent=2) if pair_explanations else 'None'}

OUTLIERS DETECTED (IQR Method):
{json.dumps(stats['outlier_counts'], indent=2)}

SAMPLE DATA (First 5 Rows):
{json.dumps(stats['sample_rows'], indent=2)}

Based on this data, provide a comprehensive analysis. 

IMPORTANT: Return ONLY valid JSON (no markdown, no extra text) with exactly these keys:
{{
    "summary": "Brief overview of the dataset (2-3 sentences)",
    "key_trends": ["List of 3-5 key trends or patterns observed"],
    "outliers": "Description of outliers found and their significance",
    "correlations": "Analysis of relationships between numeric variables",
    "missing_data_notes": "Assessment of missing data impact",
    "business_insights": ["List of 3-5 actionable business insights"],
    "recommended_next_steps": ["List of 3-5 recommended analysis or actions"]
}}

Return ONLY the JSON object, nothing else."""
    
    return prompt


def build_image_prompt(extracted_text: str, details: dict = None) -> str:
    """
    Build a prompt for explaining a chart image. `extracted_text` should contain any
    OCR results (axis labels, legend text, annotations). `details` can include
    user hints like known x/y variable names or context.
    """
    context = details or {}
    ctx_lines = []
    if 'source' in context:
        ctx_lines.append(f"Source/context: {context['source']}")
    if 'hint' in context:
        ctx_lines.append(f"User hint: {context['hint']}")

    ctx_block = "\n".join(ctx_lines)

    prompt = f"""You are an expert analyst specialized in interpreting charts and figures.

Here is extracted text from an uploaded chart image (could include axis labels, legend entries, annotations, or table snippets):

{extracted_text}

Additional context:
{ctx_block}

Please provide a detailed, structured explanation covering:
- What each axis likely represents (including units if detectable)
- What the plotted data depicts and the time/scale if present
- Key patterns, trends, and anomalies visible in the chart
- If applicable, compare series (e.g., model A vs model B) and describe which appears better on which metrics
- Possible causes for observed patterns and cautions about interpretation
- Suggested next quantitative checks or analyses to validate observations

Return ONLY valid JSON with these keys:
{
  "axis_explanation": {"x": "...", "y": "..."},
  "visual_summary": "Short paragraph summary of main story",
  "detailed_insights": ["list of detailed observations"],
  "recommended_checks": ["analysis steps to validate"],
  "confidence_notes": "notes about confidence and missing info"
}

Return only the JSON object and nothing else."""

    return prompt


def build_baseline_prompt(df: pd.DataFrame) -> str:
    """
    Build a simple baseline prompt from raw data.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        Simple prompt string with first 10 rows of data
    """
    sample_data = df.head(10).to_string()
    
    prompt = f"""You are given only a small sample of the dataset.
Provide a quick, high-level baseline analysis that avoids deep statistical interpretation.

Focus on:
- obvious patterns visible in the first 10 rows
- likely data quality issues
- simple trends or category differences
- practical next steps for a full analysis

Sample data:

{sample_data}

IMPORTANT: Return ONLY valid JSON (no markdown, no extra text) with exactly these keys:
{{
    "summary": "Brief overview based only on the sample rows (2-3 sentences)",
    "key_trends": ["List of 2-4 quick observations from the sample"],
    "outliers": "Any obvious unusual values or suspicious rows in the sample",
    "correlations": "Only mention obvious relationships if they are visible from the sample",
    "missing_data_notes": "Assessment of obvious missing data issues",
    "business_insights": ["List of 3-5 actionable business insights"],
    "recommended_next_steps": ["List of 3-5 recommended analysis or actions for a full EDA"]
}}

Return ONLY the JSON object, nothing else."""
    
    return prompt
