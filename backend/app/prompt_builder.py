import pandas as pd
from typing import Dict, Any
import json


def build_structured_prompt(stats: Dict[str, Any]) -> str:
    """
    Build a detailed, comprehensive structured prompt for Gemini from enhanced EDA stats.
    
    Args:
        stats: Dictionary from eda_engine.analyze()
    
    Returns:
        Detailed prompt string instructing Gemini to return JSON
    """
    
    # Extract key statistics
    shape = stats.get('shape', {})
    numeric_cols = stats.get('descriptive_stats', {})
    categorical_cols = stats.get('categorical_analysis', {})
    correlations = stats.get('strong_correlations', [])
    outlier_summary = stats.get('outlier_analysis', {})
    data_quality = stats.get('data_quality_score', {})
    missing_summary = stats.get('missing_data_summary', {})
    
    # Count total outliers
    total_outliers = sum(v.get('count', 0) for v in outlier_summary.values())
    
    prompt = f"""You are an expert data analyst with 15+ years of experience. Your task is to provide 
comprehensive, actionable insights from a dataset that will be used by business stakeholders (non-technical).

DATASET OVERVIEW:
- Size: {shape.get('rows')} rows × {shape.get('columns')} columns
- Data Quality Score: {data_quality.get('overall_score', 'N/A')}/100 ({data_quality.get('interpretation', 'Unknown')})
- Missing Data: {missing_summary.get('missing_percentage', 0)}% overall
- Outliers Detected: {total_outliers} unusual values

NUMERIC COLUMNS ANALYZED:
{json.dumps(numeric_cols, indent=2)}

CATEGORICAL COLUMNS:
{json.dumps(categorical_cols, indent=2)}

DISTRIBUTION PATTERNS (Skewness & Kurtosis):
{json.dumps(stats.get('distribution_analysis', {}), indent=2)}

STRONG CORRELATIONS (> 0.7):
{json.dumps(correlations, indent=2) if correlations else 'None found'}

OUTLIER ANALYSIS:
{json.dumps(outlier_summary, indent=2)}

DATA QUALITY ASSESSMENT:
- Completeness: {data_quality.get('completeness_score', 'N/A')}/100
- Outlier Quality: {data_quality.get('outlier_quality_score', 'N/A')}/100

IMPORTANT REQUIREMENTS:
1. Analyze patterns and relationships between variables
2. Identify business-relevant anomalies and outliers
3. Provide statistical significance assessments
4. Flag data quality issues that need attention
5. Suggest data preprocessing steps if needed
6. Provide actionable business recommendations

Return ONLY valid JSON (no markdown, no backticks, no extra text) with exactly these keys:

{{
    "executive_summary": "2-3 sentence overview of the dataset and its key characteristics",
    
    "data_quality_assessment": {{
        "overall_assessment": "Detailed assessment of data completeness and quality",
        "critical_issues": ["List of critical data issues that need immediate attention"],
        "recommended_cleaning": ["List of specific data cleaning or preprocessing steps"]
    }},
    
    "numeric_analysis": {{
        "central_tendency": "Analysis of mean, median values and what they indicate",
        "variability": "Discussion of std deviation, range, and data spread",
        "distribution_insights": "Analysis of skewness and kurtosis patterns",
        "key_statistics": ["Top 3-5 statistical insights from numeric columns"]
    }},
    
    "categorical_insights": {{
        "value_distributions": "Analysis of categorical variable distributions",
        "dominant_categories": ["List of most important categories and their significance"],
        "category_patterns": "Any interesting patterns or imbalances in categories"
    }},
    
    "outlier_analysis": {{
        "outlier_summary": "What outliers were found and their characteristics",
        "potential_causes": "Possible reasons for outliers (errors vs. real anomalies)",
        "business_significance": "What do these outliers mean for the business?",
        "recommended_action": "Should outliers be removed, investigated, or kept?"
    }},
    
    "correlation_insights": {{
        "strong_relationships": "Description of strong correlations found",
        "business_implications": "What these relationships mean for operations",
        "potential_causal_links": "Which relationships might indicate causation vs. correlation"
    }},
    
    "data_patterns_and_trends": [
        "Pattern 1: Description with business relevance",
        "Pattern 2: Description with business relevance",
        "Pattern 3: Description with business relevance"
    ],
    
    "anomalies_and_risks": {{
        "identified_anomalies": ["List of unusual patterns or values"],
        "risk_assessment": "Assessment of how these anomalies might affect analysis",
        "mitigation_strategies": ["Recommended actions to address anomalies"]
    }},
    
    "actionable_business_insights": [
        "Insight 1: What is it and why does it matter?",
        "Insight 2: What is it and why does it matter?",
        "Insight 3: What is it and why does it matter?",
        "Insight 4: What is it and why does it matter?",
        "Insight 5: What is it and why does it matter?"
    ],
    
    "next_steps_and_recommendations": {{
        "immediate_actions": ["Actions to take right now based on findings"],
        "deeper_analysis_needed": ["Areas that need further investigation"],
        "suggested_modeling_approaches": ["Types of analysis or models that could be applied"],
        "timeline": "Suggested timeline for implementing recommendations"
    }},
    
    "summary_metrics": {{
        "data_completeness": "{data_quality.get('completeness_score', 'N/A')}/100",
        "data_quality": "{data_quality.get('overall_score', 'N/A')}/100",
        "analysis_reliability": "Based on data quality, how reliable are these insights?"
    }}
}}

Return ONLY the JSON object. No markdown formatting. No code blocks. Raw JSON only."""
    
    return prompt


def build_simple_explanation_prompt(json_insights: Dict[str, Any]) -> str:
    """
    Build a prompt to simplify and explain complex insights for non-technical users.
    
    Args:
        json_insights: Dictionary from gemini_client with insights
    
    Returns:
        Prompt string for simplification
    """
    
    prompt = f"""You are a data communication expert. Your job is to simplify complex data insights 
for business stakeholders who have no statistics background.

Take these data insights and re-explain them using:
- Simple, everyday language
- Concrete examples and analogies
- Business-relevant context
- Clear, actionable recommendations

ORIGINAL INSIGHTS:
{json.dumps(json_insights, indent=2)}

For each insight, provide:
1. What it means in plain English (1-2 sentences)
2. Why it matters to the business (1 sentence)
3. What to do about it (1-2 sentences)

Return ONLY valid JSON with:
{{
    "simplified_insights": [
        {{
            "original": "Original insight text",
            "simplified": "Simple explanation",
            "why_it_matters": "Business relevance",
            "what_to_do": "Recommended action"
        }}
    ]
}}"""
    
    return prompt


def build_baseline_prompt(df: pd.DataFrame) -> str:
    """
    Build a simple baseline prompt from raw data (for comparison).
    
    Args:
        df: pandas DataFrame
    
    Returns:
        Simple prompt string with first 10 rows of data
    """
    
    sample_data = df.head(10).to_string()
    shape = df.shape
    
    prompt = f"""Analyze this dataset and provide insights. This is basic exploratory analysis.

DATASET SHAPE: {shape[0]} rows × {shape[1]} columns

SAMPLE DATA (First 10 rows):
{sample_data}

QUICK ANALYSIS:
1. What patterns do you see?
2. Are there obvious data quality issues?
3. What are the top 3-5 insights?
4. What should we look into next?

Return ONLY valid JSON with:
{{
    "summary": "Brief dataset overview",
    "quick_patterns": ["Pattern 1", "Pattern 2", "Pattern 3"],
    "data_quality_issues": ["Issue 1", "Issue 2"],
    "top_insights": ["Insight 1", "Insight 2", "Insight 3"],
    "next_steps": ["Action 1", "Action 2"]
}}"""
    
    return prompt


def build_comparison_prompt(baseline_insights: Dict[str, Any], 
                           advanced_insights: Dict[str, Any]) -> str:
    """
    Build a prompt to compare baseline vs. advanced analysis results.
    
    Args:
        baseline_insights: Results from baseline analysis
        advanced_insights: Results from advanced/structured analysis
    
    Returns:
        Prompt string for comparison
    """
    
    prompt = f"""Compare these two data analyses - one basic, one comprehensive.

BASELINE ANALYSIS (Simple approach):
{json.dumps(baseline_insights, indent=2)}

ADVANCED ANALYSIS (Structured approach with statistics):
{json.dumps(advanced_insights, indent=2)}

COMPARISON TASK:
1. List insights that both analyses found
2. List new insights found ONLY in the advanced analysis
3. Assess which analysis is more complete and why
4. Identify which method would be better for different use cases

Return ONLY valid JSON with:
{{
    "shared_insights": ["Common finding 1", "Common finding 2"],
    "unique_advanced_insights": ["Advanced only 1", "Advanced only 2"],
    "depth_comparison": "Which analysis is more thorough and why?",
    "reliability_assessment": "Which would be more reliable for decision-making?",
    "use_case_recommendations": "When to use which approach?"
}}"""
    
    return prompt