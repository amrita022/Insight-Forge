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


def build_baseline_prompt(df: pd.DataFrame) -> str:
    """
    Build a simple baseline prompt from raw data.
    
    Args:
        df: pandas DataFrame
    
    Returns:
        Simple prompt string with first 10 rows of data
    """
    sample_data = df.head(10).to_string()
    
    prompt = f"""Analyze this dataset and give insights:

{sample_data}

IMPORTANT: Return ONLY valid JSON (no markdown, no extra text) with exactly these keys:
{{
    "summary": "Brief overview of the dataset (2-3 sentences)",
    "key_trends": ["List of 3-5 key trends or patterns observed"],
    "outliers": "Description of outliers found and their significance",
    "correlations": "Analysis of relationships between variables",
    "missing_data_notes": "Assessment of missing data impact",
    "business_insights": ["List of 3-5 actionable business insights"],
    "recommended_next_steps": ["List of 3-5 recommended analysis or actions"]
}}

Return ONLY the JSON object, nothing else."""
    
    return prompt
