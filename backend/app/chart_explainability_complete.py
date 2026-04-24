"""
CHART EXPLAINABILITY MODULE
Generates AI-powered plain-language explanations for charts
Makes data analysis accessible to non-technical users
"""

import json
from typing import Dict, Any, List
import sys

# ============================================================================
# NOTE: If gemini_client is not available, use placeholder responses
# In production, uncomment the import below and configure your API key
# ============================================================================
# from gemini_client import call_gemini

# For now, we'll create local explanations (no API required)


class ChartExplainer:
    """Generate explanations for charts in plain, non-technical language"""
    
    def __init__(self, use_ai=False):
        """
        Initialize the chart explainer
        
        Args:
            use_ai: If True, uses Gemini API for explanations
                   If False, uses built-in explanations
        """
        self.use_ai = use_ai
    
    def explain_distribution_chart(self, column_name: str, stats: Dict[str, Any]) -> str:
        """
        Generate explanation for a distribution histogram
        
        Args:
            column_name: Name of the column
            stats: Statistical information about the column
        
        Returns:
            Plain language explanation
        """
        
        mean = stats.get('mean', 0)
        median = stats.get('median', 0)
        std = stats.get('std', 0)
        min_val = stats.get('min', 0)
        max_val = stats.get('max', 0)
        skewness = stats.get('skewness_interpretation', 'Symmetric')
        
        explanation = f"""
📊 WHAT THIS CHART SHOWS:

This histogram displays how {column_name} values are distributed across your data.
Think of it like a frequency count - taller bars mean more people/items have those values.

KEY OBSERVATIONS:
• Average ({column_name}): {mean:.2f}
  The typical value in your dataset
  
• Middle Value (Median): {median:.2f}
  The value that splits your data in half
  
• Spread (Range): {min_val:.2f} to {max_val:.2f}
  The minimum and maximum values
  
• Shape: {skewness}
  {self._interpret_skewness(skewness)}

WHAT THIS MEANS IN SIMPLE TERMS:
The chart shows whether your {column_name} values are:
✓ Clustered around one area (concentrated)
✓ Spread out evenly (distributed)
✓ Skewed to one side (unbalanced)

BUSINESS INSIGHT:
Use this to understand if {column_name} values are typical and normal,
or if there are unusual patterns you should investigate.
"""
        
        return explanation.strip()
    
    def explain_boxplot(self, column_name: str, stats: Dict[str, Any]) -> str:
        """
        Generate explanation for a boxplot
        
        Args:
            column_name: Name of the column
            stats: Statistical information including Q1, Q3, median
        
        Returns:
            Plain language explanation
        """
        
        q1 = stats.get('q1', 0)
        median = stats.get('median', 0)
        q3 = stats.get('q3', 0)
        outlier_count = stats.get('outlier_count', 0)
        outlier_percentage = stats.get('outlier_percentage', 0)
        
        explanation = f"""
📦 WHAT THIS BOXPLOT SHOWS:

A boxplot is like a snapshot that shows where most of your {column_name} values are
and highlights any unusual values (outliers).

PARTS OF THE BOXPLOT:
┌─────────────────────────────────────────┐
│                                         │
│  THE BOX: Contains the middle 50%       │
│  Line in box: The median (middle value) │
│  Whiskers: The normal range             │
│  Dots: Outliers (unusual values)        │
│                                         │
└─────────────────────────────────────────┘

YOUR DATA:
• Bottom of box (Q1): {q1:.2f} - 25% of values are below this
• Middle line: {median:.2f} - This is the median (half above, half below)
• Top of box (Q3): {q3:.2f} - 75% of values are below this
• Outliers found: {outlier_count} ({outlier_percentage}%)

WHAT THIS MEANS:
If the box is:
✓ Tall and wide = Values are very different from each other
✓ Short and narrow = Values are similar to each other
✓ Has dots outside = Some unusual/extreme values exist

WHY IT MATTERS:
Outliers could be:
• Real problems or opportunities (investigate)
• Data entry errors (fix them)
• Just natural variation (keep them)

RECOMMENDATION:
{self._outlier_recommendation(outlier_percentage)}
"""
        
        return explanation.strip()
    
    def explain_correlation_heatmap(self, correlations: List[Dict], 
                                   total_variables: int) -> str:
        """
        Generate explanation for a correlation heatmap
        
        Args:
            correlations: List of strong correlations found
            total_variables: Total number of variables analyzed
        
        Returns:
            Plain language explanation
        """
        
        explanation = f"""
🔗 WHAT THIS CORRELATION CHART SHOWS:

Correlation measures whether two variables "move together".

SIMPLE EXAMPLE:
If ice cream sales and temperature both increase together = Positive correlation
If umbrella sales decrease when weather improves = Negative correlation

COLOR MEANINGS:
• Red/Warm colors: Positive correlation (both increase together)
• Blue/Cool colors: Negative correlation (one increases, other decreases)
• White/Light colors: No relationship (one doesn't affect the other)

STRONG CORRELATIONS FOUND IN YOUR DATA:
"""
        
        if correlations:
            for i, corr in enumerate(correlations, 1):
                var1 = corr.get('variable1', 'Variable A')
                var2 = corr.get('variable2', 'Variable B')
                value = corr.get('correlation', 0)
                interpretation = self._interpret_correlation(value)
                
                explanation += f"""
{i}. {var1} ↔ {var2}: {value:.3f}
   {interpretation}
"""
        else:
            explanation += """
No strong correlations found (threshold > 0.7)
This means your variables don't strongly influence each other.
"""
        
        explanation += f"""

WHY THIS MATTERS:
✓ Strong correlations indicate variable relationships
✓ Helps identify what drives changes in your business
✓ Reveals dependencies between metrics
✓ Important for building predictive models

IMPORTANT NOTE:
⚠️ Correlation does NOT mean causation!
Just because two things move together doesn't mean one causes the other.
"""
        
        return explanation.strip()
    
    def explain_missing_data(self, missing_summary: Dict[str, Any], 
                            missing_by_column: Dict[str, Any]) -> str:
        """
        Generate explanation for missing data visualization
        
        Args:
            missing_summary: Overall missing data statistics
            missing_by_column: Missing data per column
        
        Returns:
            Plain language explanation
        """
        
        total_missing_pct = missing_summary.get('missing_percentage', 0)
        total_missing = missing_summary.get('total_missing', 0)
        
        explanation = f"""
❌ WHAT MISSING DATA MEANS:

Missing data = Empty cells in your dataset
These are values that were not recorded or are unknown.

OVERALL PICTURE:
• Total missing values: {total_missing} cells
• Percentage of total: {total_missing_pct}% of all data
• Status: {self._missing_data_status(total_missing_pct)}

MISSING DATA BY COLUMN:
"""
        
        # Sort columns by missing percentage (highest first)
        sorted_cols = sorted(missing_by_column.items(), 
                           key=lambda x: x[1].get('percentage', 0), 
                           reverse=True)
        
        for col_name, col_data in sorted_cols[:10]:  # Top 10
            missing_count = col_data.get('count', 0)
            missing_pct = col_data.get('percentage', 0)
            if missing_pct > 0:
                explanation += f"\n• {col_name}: {missing_count} missing ({missing_pct}%)"
        
        explanation += f"""

IMPACT ASSESSMENT:
"""
        
        if total_missing_pct < 5:
            explanation += "✅ LOW IMPACT: Your data is very complete"
        elif total_missing_pct < 20:
            explanation += "⚠️ MODERATE: Some gaps exist but manageable"
        else:
            explanation += "❌ HIGH IMPACT: Significant gaps need attention"
        
        explanation += """

RECOMMENDATIONS:
1. Columns with > 30% missing: Consider removing or imputing
2. Columns with < 5% missing: Safe to delete/fill
3. Investigate WHEN/WHY data is missing
   - Is it random or systematic?
   - Can you find the missing values elsewhere?

HOW TO HANDLE:
• Delete rows with missing values (if few)
• Fill with average/median (if numeric)
• Fill with "Unknown" (if categorical)
• Use advanced imputation methods
"""
        
        return explanation.strip()
    
    def explain_categorical_distribution(self, column_name: str, 
                                        categories: Dict[str, int]) -> str:
        """
        Generate explanation for categorical data distribution
        
        Args:
            column_name: Name of the categorical column
            categories: Dictionary of categories and their counts
        
        Returns:
            Plain language explanation
        """
        
        total_count = sum(categories.values())
        
        explanation = f"""
🏷️ WHAT THIS CATEGORICAL CHART SHOWS:

This chart shows how {column_name} values are distributed.
Each bar represents a category and how many items fall into it.

DATA BREAKDOWN:
"""
        
        for category, count in sorted(categories.items(), 
                                     key=lambda x: x[1], 
                                     reverse=True)[:10]:
            percentage = (count / total_count * 100) if total_count > 0 else 0
            bar_length = int(percentage / 5)  # Each # = 5%
            bar = "█" * bar_length + "░" * (20 - bar_length)
            explanation += f"\n• {category}: {count:,} [{bar}] {percentage:.1f}%"
        
        explanation += f"""

OBSERVATIONS:
✓ Most common: {max(categories.items(), key=lambda x: x[1])[0]}
✓ Least common: {min(categories.items(), key=lambda x: x[1])[0]}
✓ Total categories: {len(categories)}
✓ Total items: {total_count:,}

BALANCE CHECK:
"""
        
        max_pct = max((count / total_count * 100) for count in categories.values()) if total_count > 0 else 0
        min_pct = min((count / total_count * 100) for count in categories.values()) if total_count > 0 else 100
        balance_ratio = max_pct / min_pct if min_pct > 0 else float('inf')
        
        if balance_ratio < 2:
            explanation += "✅ BALANCED: Categories are evenly distributed"
        elif balance_ratio < 5:
            explanation += "⚠️ SLIGHTLY IMBALANCED: Some categories more common"
        else:
            explanation += "❌ HIGHLY IMBALANCED: One category dominates"
        
        explanation += f"""

WHY IT MATTERS:
✓ Understand customer/product distribution
✓ Identify underrepresented groups
✓ Plan targeted strategies for each category
✓ Ensure data balance for analysis

NEXT STEPS:
- If imbalanced: Investigate why
- Plan strategies for underrepresented categories
- Consider if this affects your analysis
"""
        
        return explanation.strip()
    
    def generate_interpretation_guide(self) -> Dict[str, str]:
        """
        Generate a beginner's guide for understanding different chart types
        
        Returns:
            Dictionary with guides for different chart types
        """
        
        guides = {
            'histogram': """
📊 HOW TO READ A HISTOGRAM (Distribution Chart)

PARTS:
1. X-axis (horizontal): The range of values
2. Y-axis (vertical): How many times each value appears
3. Bars: Taller = more occurrences

SHAPE MEANINGS:
• Single peak in middle: Normal distribution (good!)
• Spread across range: Values vary widely
• Peak on left: Left-skewed (more low values)
• Peak on right: Right-skewed (more high values)
• Multiple peaks: Possible different groups mixed

WHAT TO LOOK FOR:
✓ Is it concentrated or spread out?
✓ Are there gaps or empty areas?
✓ Does the shape seem natural or odd?

ACTION ITEMS:
- Wide spread = More variability, plan accordingly
- Tight cluster = Values are similar
- Multiple peaks = Might have different groups to analyze
""",
            
            'boxplot': """
📦 HOW TO READ A BOXPLOT (Box & Whisker Plot)

PARTS:
1. Box: Middle 50% of your data
2. Line in box: The median (middle value)
3. Whiskers: Lines extending from box (normal range)
4. Dots: Outliers (unusual values)

INTERPRETING THE BOX:
• Tall box = Values vary widely
• Short box = Values are similar
• Line in middle = Median
• Line off-center = Skewed distribution

INTERPRETING THE WHISKERS:
• Long whiskers = Wide normal range
• Short whiskers = Narrow normal range
• Extends far = More extreme values exist

OUTLIERS (Dots):
• Points beyond whiskers = Unusual/extreme values
• Few outliers = Mostly normal values
• Many outliers = Varied data or measurement issues

ACTION ITEMS:
- Few outliers = Data looks clean
- Many outliers = Investigate the causes
- Understand if outliers are errors or valid data
""",
            
            'correlation': """
🔗 HOW TO READ A CORRELATION HEATMAP

COLORS:
• Red/Dark Red: Strong positive correlation (both increase together)
  Example: Height and weight
  
• Blue/Dark Blue: Strong negative correlation (one increases, other decreases)
  Example: Price and demand
  
• White/Light: No correlation (no relationship)

READING THE GRID:
1. Find your two variables (one on top, one on side)
2. Look at the color where they meet
3. Check the number (-1 to +1)

CORRELATION STRENGTH:
• 0.9 to 1.0: Very strong positive
• 0.7 to 0.9: Strong positive
• 0.5 to 0.7: Moderate positive
• 0.3 to 0.5: Weak positive
• -0.3 to 0.3: No relationship
• -0.5 to -0.3: Weak negative
• -0.7 to -0.5: Moderate negative
• -0.9 to -0.7: Strong negative
• -1.0 to -0.9: Very strong negative

IMPORTANT:
⚠️ Correlation ≠ Causation!
Just because two things correlate doesn't mean one causes the other.

ACTION ITEMS:
- Strong correlations = Variables move together
- Investigate: Is there a causal relationship?
- Use for predictions or understanding dependencies
""",
            
            'missing_data': """
❌ HOW TO UNDERSTAND MISSING DATA

WHAT IT MEANS:
Missing data = Empty cells that should have values

TYPES:
1. Missing Completely at Random (MCAR)
   - Nothing is causing the missing values
   - Best case scenario
   
2. Missing at Random (MAR)
   - Missing due to some other variable
   - Example: High earners less likely to report income
   
3. Not Missing at Random (NMAR)
   - Missing values related to the values themselves
   - Worst case: Biases your analysis

IMPACT:
• 1-5% missing: Usually OK, can ignore
• 5-20% missing: Can be handled (fill or remove rows)
• 20%+ missing: Requires investigation, may bias results

SOLUTIONS:
1. Delete rows with missing values
   - Pros: Simple, clean
   - Cons: Lose data
   
2. Fill with average/median
   - Pros: Keeps data size
   - Cons: Distorts distribution
   
3. Fill with forward/backward fill (time series)
   - Pros: Maintains trends
   - Cons: Not always appropriate
   
4. Use advanced imputation
   - Pros: More accurate
   - Cons: Complex

ACTION ITEMS:
- Identify which columns have missing data
- Understand the pattern (random or systematic?)
- Choose appropriate handling method
""",
            
            'categorical': """
🏷️ HOW TO READ CATEGORICAL DISTRIBUTION CHART

PARTS:
1. Categories: Different values/groups (on one axis)
2. Counts: Number of items in each category (on other axis)
3. Bars: Length shows relative frequency

INTERPRETING:
• Tall bars = More items in that category
• Short bars = Fewer items in that category
• Even heights = Balanced distribution
• Very uneven = One category dominates

BALANCE ASSESSMENT:
• Balanced: All categories roughly equal size
• Slightly imbalanced: Biggest 2-3x smallest
• Highly imbalanced: Biggest 10x+ smallest
• Very skewed: One category > 50% of total

WHAT TO LOOK FOR:
✓ Is data evenly distributed?
✓ Are some categories missing?
✓ Is one category dominating?
✓ Are there unexpected patterns?

ACTION ITEMS:
- Balanced = Good for fair analysis
- Imbalanced = May need special handling
- Investigate: Why is distribution uneven?
- Plan strategies for each category
"""
        }
        
        return guides
    
    def generate_data_quality_explanation(self, quality_score: Dict[str, Any]) -> str:
        """
        Generate plain language explanation of data quality score
        
        Args:
            quality_score: Data quality metrics
        
        Returns:
            Plain language explanation
        """
        
        overall_score = quality_score.get('overall_score', 0)
        completeness = quality_score.get('completeness_score', 0)
        outlier_quality = quality_score.get('outlier_quality_score', 0)
        interpretation = quality_score.get('interpretation', 'Unknown')
        
        explanation = f"""
📈 DATA QUALITY REPORT

OVERALL SCORE: {overall_score}/100 - {interpretation.upper()}

What does this mean?
├─ 80-100: ✅ EXCELLENT - Data is clean and ready for analysis
├─ 60-80:  ✅ GOOD - Minor issues, but usable
├─ 40-60:  ⚠️  FAIR - Some cleaning needed
└─ 0-40:   ❌ POOR - Significant work required

YOUR BREAKDOWN:
• Completeness Score: {completeness}/100
  {self._completeness_interpretation(completeness)}

• Outlier Quality: {outlier_quality}/100
  {self._outlier_quality_interpretation(outlier_quality)}

WHAT TO DO NEXT:
"""
        
        if overall_score >= 80:
            explanation += """
✅ Your data is excellent! You can:
   1. Proceed with analysis immediately
   2. Trust the results from this dataset
   3. Focus on getting insights
"""
        elif overall_score >= 60:
            explanation += """
✅ Your data is good but has minor issues. You should:
   1. Be aware of potential bias
   2. Note any gaps in the analysis
   3. Consider mentioning limitations
"""
        elif overall_score >= 40:
            explanation += """
⚠️ Your data has issues. You should:
   1. Clean the data (handle missing values)
   2. Investigate outliers
   3. Document all changes made
   4. Note limitations in conclusions
"""
        else:
            explanation += """
❌ Your data needs significant work. You should:
   1. Investigate root causes of missing data
   2. Clean and validate data thoroughly
   3. Consider if dataset is usable
   4. Document all assumptions made
"""
        
        return explanation.strip()
    
    # ===== HELPER METHODS =====
    
    def _interpret_skewness(self, skewness_text: str) -> str:
        """Provide interpretation of skewness"""
        interpretations = {
            'Fairly Symmetric': 'Your values are balanced on both sides',
            'Right Skewed (Positive)': 'You have more low values with some high outliers',
            'Left Skewed (Negative)': 'You have more high values with some low outliers'
        }
        return interpretations.get(skewness_text, '')
    
    def _interpret_correlation(self, value: float) -> str:
        """Provide business interpretation of correlation value"""
        abs_val = abs(value)
        direction = "positive (both increase)" if value > 0 else "negative (opposite)"
        
        if abs_val > 0.9:
            return f"VERY STRONG {direction} relationship - these move almost identically"
        elif abs_val > 0.7:
            return f"STRONG {direction} relationship - these tend to move together"
        elif abs_val > 0.5:
            return f"MODERATE {direction} relationship - some connection exists"
        elif abs_val > 0.3:
            return f"WEAK {direction} relationship - slight connection"
        else:
            return "NO meaningful relationship"
    
    def _outlier_recommendation(self, percentage: float) -> str:
        """Recommend action based on outlier percentage"""
        if percentage == 0:
            return "✅ No outliers found - data looks clean!"
        elif percentage < 1:
            return "✅ Very few outliers (< 1%) - normal variation, data is clean"
        elif percentage < 5:
            return "✓ Reasonable number of outliers (1-5%) - investigate but may be valid"
        else:
            return "⚠️ Many outliers (> 5%) - investigate thoroughly before analysis"
    
    def _missing_data_status(self, percentage: float) -> str:
        """Determine status based on missing percentage"""
        if percentage < 2:
            return "✅ Excellent - Almost no missing data"
        elif percentage < 5:
            return "✅ Good - Minimal missing data"
        elif percentage < 20:
            return "✓ Acceptable - Can be handled"
        elif percentage < 50:
            return "⚠️ Significant - Needs attention"
        else:
            return "❌ Critical - Needs major cleaning"
    
    def _completeness_interpretation(self, score: float) -> str:
        """Interpret completeness score"""
        if score >= 95:
            return "Nearly perfect - almost no missing values"
        elif score >= 80:
            return "Good - only a few missing values"
        elif score >= 60:
            return "Acceptable - some gaps exist"
        else:
            return "Poor - many missing values"
    
    def _outlier_quality_interpretation(self, score: float) -> str:
        """Interpret outlier quality score"""
        if score >= 90:
            return "Excellent - almost no outliers"
        elif score >= 75:
            return "Good - few outliers"
        elif score >= 50:
            return "Moderate - noticeable outliers"
        else:
            return "Poor - many outliers"


# ============================================================================
# MAIN FUNCTIONS FOR EASY USE
# ============================================================================

def generate_all_chart_explanations(eda_stats: Dict[str, Any], 
                                   chart_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Generate explanations for all charts
    
    Args:
        eda_stats: Statistics from EDA engine
        chart_data: Chart data from charts module
    
    Returns:
        Dictionary of chart explanations
    """
    
    explainer = ChartExplainer()
    explanations = {}
    
    # Distribution explanations
    if 'distributions' in chart_data:
        for dist in chart_data['distributions']:
            col_name = dist.get('column', 'Unknown')
            col_stats = eda_stats.get('descriptive_stats', {}).get(col_name, {})
            dist_analysis = eda_stats.get('distribution_analysis', {}).get(col_name, {})
            
            combined_stats = {**col_stats, **dist_analysis}
            explanations[f'distribution_{col_name}'] = explainer.explain_distribution_chart(
                col_name, combined_stats
            )
    
    # Boxplot explanations
    if 'boxplots' in chart_data:
        outlier_info = eda_stats.get('outlier_analysis', {})
        for boxplot in chart_data['boxplots']:
            col_name = boxplot.get('column', 'Unknown')
            col_stats = eda_stats.get('descriptive_stats', {}).get(col_name, {})
            col_outliers = outlier_info.get(col_name, {})
            
            combined_stats = {**col_stats}
            combined_stats['outlier_count'] = col_outliers.get('count', 0)
            combined_stats['outlier_percentage'] = col_outliers.get('percentage', 0)
            
            explanations[f'boxplot_{col_name}'] = explainer.explain_boxplot(
                col_name, combined_stats
            )
    
    # Correlation explanation
    if chart_data.get('correlation'):
        strong_corr = eda_stats.get('strong_correlations', [])
        numeric_cols = list(eda_stats.get('descriptive_stats', {}).keys())
        explanations['correlation_heatmap'] = explainer.explain_correlation_heatmap(
            strong_corr, len(numeric_cols)
        )
    
    # Missing data explanation
    if chart_data.get('missing_data_heatmap'):
        missing_summary = eda_stats.get('missing_data_summary', {})
        missing_by_col = eda_stats.get('missing_values', {})
        explanations['missing_data'] = explainer.explain_missing_data(
            missing_summary, missing_by_col
        )
    
    # Categorical explanations
    if 'categorical_distributions' in chart_data:
        cat_analysis = eda_stats.get('categorical_analysis', {})
        for cat_chart in chart_data['categorical_distributions']:
            col_name = cat_chart.get('column', 'Unknown')
            cat_dist = cat_analysis.get(col_name, {}).get('value_distribution', {})
            
            explanations[f'categorical_{col_name}'] = explainer.explain_categorical_distribution(
                col_name, cat_dist
            )
    
    return explanations


def generate_dataset_summary(eda_stats: Dict[str, Any]) -> str:
    """
    Generate plain-language summary of entire dataset
    
    Args:
        eda_stats: Statistics from EDA engine
    
    Returns:
        Plain language summary
    """
    
    shape = eda_stats.get('shape', {})
    quality = eda_stats.get('data_quality_score', {})
    missing = eda_stats.get('missing_data_summary', {})
    numeric_cols = eda_stats.get('descriptive_stats', {})
    
    summary = f"""
📊 YOUR DATASET AT A GLANCE

SIZE:
• Records: {shape.get('rows', 0):,} (rows)
• Fields: {shape.get('columns', 0)} (columns)
• Total data points: {shape.get('rows', 0) * shape.get('columns', 0):,}

QUALITY:
• Overall Score: {quality.get('overall_score', 0)}/100 ({quality.get('interpretation', 'Unknown')})
• Complete Data: {quality.get('completeness_score', 0)}%
• Outlier Quality: {quality.get('outlier_quality_score', 0)}%

DATA COMPLETENESS:
• Missing Values: {missing.get('total_missing', 0)} cells
• Missing Percentage: {missing.get('missing_percentage', 0)}%

NUMERIC FIELDS FOUND: {len(numeric_cols)}
CATEGORICAL FIELDS: {len(eda_stats.get('categorical_analysis', {}))}

STRONG RELATIONSHIPS:
Found {len(eda_stats.get('strong_correlations', []))} strong correlations

UNUSUAL VALUES:
Found {eda_stats.get('total_outliers', 0)} outliers in total

READINESS FOR ANALYSIS:
"""
    
    explainer = ChartExplainer()
    quality_exp = explainer.generate_data_quality_explanation(quality)
    summary += quality_exp
    
    return summary


def get_interpretation_guides() -> Dict[str, str]:
    """
    Get beginner's guides for all chart types
    
    Returns:
        Dictionary with interpretation guides
    """
    explainer = ChartExplainer()
    return explainer.generate_interpretation_guide()


if __name__ == "__main__":
    # Test the explainer with sample data
    print("Chart Explainability Module Test")
    print("=" * 50)
    
    # Create sample statistics
    sample_stats = {
        'mean': 45.3,
        'median': 44.0,
        'std': 12.5,
        'min': 18,
        'max': 80,
        'q1': 35,
        'q3': 55,
        'skewness_interpretation': 'Fairly Symmetric'
    }
    
    # Test distribution explanation
    explainer = ChartExplainer()
    print("\n1. DISTRIBUTION CHART EXPLANATION:")
    print("-" * 50)
    dist_exp = explainer.explain_distribution_chart('age', sample_stats)
    print(dist_exp)
    
    # Test boxplot explanation
    print("\n2. BOXPLOT EXPLANATION:")
    print("-" * 50)
    boxplot_exp = explainer.explain_boxplot('age', {**sample_stats, 'outlier_count': 3, 'outlier_percentage': 1.2})
    print(boxplot_exp)
    
    # Test interpretation guides
    print("\n3. INTERPRETATION GUIDES:")
    print("-" * 50)
    guides = explainer.generate_interpretation_guide()
    for guide_type, guide_text in guides.items():
        print(f"\n{guide_type.upper()}:")
        print(guide_text[:200] + "...")