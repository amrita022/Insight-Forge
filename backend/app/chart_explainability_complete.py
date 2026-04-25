"""
INSIGHT-FORGE: CHART EXPLAINABILITY MODULE (Full Edition)
==========================================================
Plain-language explanations for every chart type.
Designed so non-technical stakeholders understand
WHY each chart exists and WHAT to do with the insight.

Supported:
  Distribution Histogram | KDE | Scatter | Line | Categorical Bar
  Box Plot | Violin | Correlation Heatmap | Pair Plot
  Bubble Chart | Pie/Donut | Missing Data | Summary Dashboard
"""

from __future__ import annotations
from typing import Any, Dict, List, Optional


# ── helpers ──────────────────────────────────────────────────────────────────

def _skew_interp(val: Optional[float]) -> str:
    if val is None:
        return "shape unknown"
    if abs(val) < 0.5:
        return "fairly symmetric – similar to a bell curve"
    if val > 0:
        return f"right-skewed ({val:.2f}) – most values are low, a few are very high"
    return f"left-skewed ({val:.2f}) – most values are high, a few are very low"

def _corr_strength(r: float) -> str:
    a = abs(r)
    sign = "positive" if r >= 0 else "negative"
    if a >= 0.9:
        return f"very strong {sign} relationship"
    if a >= 0.7:
        return f"strong {sign} relationship"
    if a >= 0.5:
        return f"moderate {sign} relationship"
    if a >= 0.3:
        return f"weak {sign} relationship"
    return "very weak or no relationship"

def _missing_severity(pct: float) -> str:
    if pct < 2:   return "Excellent – almost no missing data"
    if pct < 10:  return "Good – minor gaps, easy to handle"
    if pct < 25:  return "⚠️ Moderate – needs imputation or investigation"
    if pct < 50:  return "⚠️ High – significant data loss, proceed with caution"
    return " Critical – column may be unusable"

def _outlier_advice(pct: float) -> str:
    if pct == 0:    return "Clean – no outliers detected"
    if pct < 1:     return "Minimal outliers (< 1%) – likely natural variation"
    if pct < 5:     return "ℹSome outliers (1–5%) – investigate before modelling"
    return "⚠️ Many outliers (> 5%) – review data collection or apply transformations"


# ── per-chart explanation functions ──────────────────────────────────────────

def explain_histogram(column: str, stats: Dict[str, Any]) -> str:
    mean    = stats.get("mean", 0)
    median  = stats.get("median", 0)
    std     = stats.get("std", 0)
    min_v   = stats.get("min", 0)
    max_v   = stats.get("max", 0)
    skew    = _skew_interp(stats.get("skewness"))

    diff = abs(mean - median)
    balance = (
        f"The mean ({mean:.2f}) and median ({median:.2f}) are close, "
        "so extreme values are not pulling the average much."
        if diff < std * 0.25
        else f"The mean ({mean:.2f}) and median ({median:.2f}) differ by {diff:.2f}. "
             "This gap suggests that a few extreme values are pulling the average."
    )

    return f"""📊 DISTRIBUTION HISTOGRAM — {column.upper()}

WHAT THIS CHART IS:
  A histogram shows how often different values appear.
  Taller bars = more records have that value.
  Think of it like a "popularity contest" for numbers.

KEY NUMBERS:
  • Average (Mean): {mean:.2f}
  • Middle value (Median): {median:.2f}
  • Typical spread (Std Dev): ± {std:.2f}
  • Full range: {min_v:.2f}  →  {max_v:.2f}

SHAPE OF THE DATA:
  The distribution is {skew}.

MEAN vs. MEDIAN:
  {balance}

WHY THIS MATTERS:
  • A symmetric shape means the data behaves predictably.
  • A skewed shape means a small group of extreme values could
    distort averages and mislead reports.
  • Use the MEDIAN (not the mean) for skewed data.

SUGGESTED ACTION:
  {"No action needed – distribution looks healthy." if abs(stats.get("skewness", 0) or 0) < 0.5
   else "Consider log-transforming this column before statistical modelling."}
"""

def explain_kde(column: str, stats: Dict[str, Any]) -> str:
    mean = stats.get("mean", 0)
    std  = stats.get("std", 0)
    return f"""〰️ KDE DENSITY CURVE — {column.upper()}

WHAT THIS CHART IS:
  A KDE (Kernel Density Estimate) is a smoothed version of the histogram.
  Instead of bars, it draws a continuous curve showing where values
  are most concentrated.  The higher the curve, the more common
  those values are.

HOW TO READ IT:
  • Peaks → most common values
  • Wide flat sections → values spread out broadly
  • Sharp narrow peaks → values cluster tightly

YOUR DATA:
  • Average: {mean:.2f}
  • Spread:  ± {std:.2f}

COMPARED TO A HISTOGRAM:
  KDE is better for spotting multiple "humps" (bi-modal distributions)
  which suggest two different sub-groups exist in your data.

SUGGESTED ACTION:
  {"Single peak – data appears to follow one group." if std < mean * 0.5
   else "Wide spread – consider checking if sub-groups exist (e.g., by region or category)."}
"""

def explain_scatter(x_col: str, y_col: str, corr: float) -> str:
    strength = _corr_strength(corr)
    return f"""🔵 SCATTER PLOT — {x_col.upper()}  vs  {y_col.upper()}

WHAT THIS CHART IS:
  Each dot represents one record.  Its horizontal position shows
  the value of {x_col} and its vertical position shows {y_col}.
  The trend line summarises the overall pattern.

CORRELATION FOUND: r = {corr:.3f}
  This is a {strength}.

HOW TO INTERPRET r:
  r = +1.0 → Perfect increase together
  r =  0.0 → No relationship at all
  r = -1.0 → Perfect inverse (one rises, other falls)

YOUR RESULT ({corr:.3f}):
  {
    "As " + x_col + " increases, " + y_col + " also tends to increase."
    if corr > 0.3
    else "As " + x_col + " increases, " + y_col + " tends to decrease."
    if corr < -0.3
    else x_col + " and " + y_col + " do not appear strongly related."
  }

⚠️  IMPORTANT:
  Correlation ≠ Causation.  Even a strong r does not mean one variable
  *causes* the other to change.  Always seek a business explanation.

SUGGESTED ACTION:
  {"Investigate this relationship further – it may be predictively useful." if abs(corr) > 0.5
   else "No strong relationship found – these variables may be independent."}
"""

def explain_line(column: str) -> str:
    return f"""📈 LINE CHART — {column.upper()} over Record Index

WHAT THIS CHART IS:
  This chart plots {column} values in the order they appear in your dataset.
  It is useful for spotting trends, cycles, or sudden jumps over time
  (or over record sequence if no date column exists).

HOW TO READ IT:
  • Rising line    → values increasing over time/records
  • Falling line   → values decreasing
  • Zigzag pattern → high variability / seasonality
  • Flat line      → stable, little change

WHY THIS MATTERS:
  Line charts reveal whether a metric is improving or declining,
  which bar charts or histograms cannot show.

SUGGESTED ACTION:
  If you see a clear trend, consider time-series forecasting.
  Sudden spikes or drops may indicate data entry errors or real events
  that need investigation.
"""

def explain_categorical_bar(column: str, top_cat: str, top_count: int,
                             n_unique: int) -> str:
    return f"""📊 COUNT BAR CHART — {column.upper()}

WHAT THIS CHART IS:
  Each bar shows how many records belong to one category.
  Taller bar = more records in that group.

YOUR DATA:
  • Distinct categories: {n_unique}
  • Most common value:   "{top_cat}"  ({top_count:,} records)

HOW TO READ IT:
  • Balanced bars → data is evenly spread across categories
  • One dominant bar → one category dominates; models may be biased
  • Many tiny bars → consider grouping rare categories into "Other"

WHY THIS MATTERS:
  Category imbalance (e.g., 90% Active, 10% Inactive) can make
  machine learning models biased toward the dominant class.

SUGGESTED ACTION:
  {"Data looks reasonably balanced across categories." if n_unique <= 8
   else "Many categories present – consider grouping rare ones (< 2%) into 'Other'."}
"""

def explain_boxplot(column: str, q1: float, median: float, q3: float,
                    outlier_count: int, outlier_pct: float) -> str:
    iqr = q3 - q1
    advice = _outlier_advice(outlier_pct)
    return f"""📦 BOX PLOT — {column.upper()}

WHAT THIS CHART IS:
  A box plot (also called box-and-whisker) compresses all key
  statistics into one compact picture.

ANATOMY OF THE BOX:
  ┌──────────────────────────────────────┐
  │  Whisker top   = upper "normal" limit│
  │  Top of box    = Q3 (75th percentile)│
  │  Line in box   = Median (50%)        │
  │  Bottom of box = Q1 (25th percentile)│
  │  Whisker bottom= lower "normal" limit│
  │  Dots outside  = Outliers            │
  └──────────────────────────────────────┘

YOUR DATA:
  • Q1 (bottom 25%):     {q1:.2f}
  • Median (middle):     {median:.2f}
  • Q3 (top 25%):        {q3:.2f}
  • IQR (box height):    {iqr:.2f}
  • Outliers:            {outlier_count} records ({outlier_pct:.1f}%)

OUTLIER VERDICT:
  {advice}

SUGGESTED ACTION:
  {"All good – no outliers to investigate." if outlier_count == 0
   else "Review outlier records individually – they may be data errors or genuine anomalies."}
"""

def explain_violin(column: str, cat_column: Optional[str] = None) -> str:
    group_note = (
        f"  The plot is split by **{cat_column}** so you can compare distributions across groups."
        if cat_column
        else "  A single group violin is shown (no categorical grouping column found)."
    )
    return f"""🎻 VIOLIN PLOT — {column.upper()}

WHAT THIS CHART IS:
  A violin plot combines a box plot with a KDE density curve.
  It shows the full shape of the distribution, not just summary stats.

HOW TO READ IT:
  • Wide sections → many values concentrated there
  • Narrow sections → few values in that range
  • The white dot inside = the median
  • The thick bar = the interquartile range (IQR)

{group_note}

COMPARED TO A BOX PLOT:
  Box plots hide multi-modal distributions; violin plots reveal them.
  If you see a "double bump" shape, two sub-groups likely exist.

WHY THIS MATTERS:
  You can immediately see whether different groups
  (e.g., regions, customer types) have different value distributions —
  critical for fair, group-aware analysis.

SUGGESTED ACTION:
  Look for groups whose violin shape differs markedly from others;
  those groups may need separate models or policies.
"""

def explain_correlation_heatmap(strong_corrs: List[Dict]) -> str:
    if strong_corrs:
        pairs = "\n".join(
            f"  • {c['variable1']} ↔ {c['variable2']}: r = {c['correlation']:.3f}  "
            f"({_corr_strength(c['correlation'])})"
            for c in strong_corrs[:8]
        )
    else:
        pairs = "  None found above the 0.7 threshold."

    return f"""🌡️ CORRELATION HEATMAP

WHAT THIS CHART IS:
  The heatmap shows the correlation coefficient (r) between every pair
  of numeric variables simultaneously.

COLOR GUIDE:
  🔴 Dark red  → Strong positive correlation (both rise together)
  🔵 Dark blue → Strong negative correlation (one rises, other falls)
  ⚪ White     → No meaningful relationship

HOW TO READ NUMBERS:
  +1.0  = Perfect positive link
   0.0  = No link
  −1.0  = Perfect inverse link

STRONG CORRELATIONS IN YOUR DATA (|r| > 0.7):
{pairs}

WHY THIS MATTERS:
  • High correlations can indicate redundant features in a model
    (multicollinearity) — keeping both may cause confusion.
  • It reveals which variables drive each other, helping you focus
    on the most impactful levers.

⚠️  REMEMBER:
  Correlation ≠ Causation.  Always validate with domain knowledge.

SUGGESTED ACTION:
  {"Consider removing one variable from each highly correlated pair when building predictive models." if strong_corrs
   else "No action needed – variables appear independent of each other."}
"""

def explain_pair_plot(columns: List[str], hue: Optional[str]) -> str:
    hue_note = (
        f"  Dots are color-coded by **{hue}** for group comparison."
        if hue
        else "  No categorical color-coding applied."
    )
    return f"""🔢 PAIR PLOT — Multi-variable View

WHAT THIS CHART IS:
  A pair plot shows every possible scatter plot between your selected
  numeric columns in one grid.  The diagonal cells show the distribution
  (KDE) of each individual column.

COLUMNS SHOWN: {', '.join(columns)}

{hue_note}

HOW TO READ IT:
  • Diagonal (top-left to bottom-right) → density curve for each variable
  • Off-diagonal cells → scatter plots between each pair
  • A tight linear pattern → strong correlation
  • A cloud of dots       → weak or no correlation

WHY THIS MATTERS:
  You can survey ALL variable relationships at once without clicking
  through many individual scatter plots.  It's the fastest way to
  spot interesting patterns before deeper analysis.

SUGGESTED ACTION:
  Identify the 1–3 scatter cells with the clearest pattern and
  follow up with individual scatter plots for deeper inspection.
"""

def explain_bubble(x_col: str, y_col: str, size_col: str) -> str:
    return f"""🫧 BUBBLE CHART — {x_col}  vs  {y_col}  (size = {size_col})

WHAT THIS CHART IS:
  Like a scatter plot, but with a THIRD dimension:
  the SIZE of each bubble represents the value of {size_col}.

  • Horizontal position → {x_col}
  • Vertical position   → {y_col}
  • Bubble size         → {size_col}
  • Bubble color (if shown) → category group

HOW TO READ IT:
  • Large bubbles in the top-right → high values on all three metrics
  • Clusters of small bubbles → a group with low {size_col}
  • Outlier bubbles far from the rest → investigate those records

WHY THIS MATTERS:
  Three variables in one chart helps with prioritisation.
  For example: "Which customer segments have high spending
  but low engagement?" becomes visually obvious.

SUGGESTED ACTION:
  Identify any large bubbles that sit in an unexpected location
  — they represent high-impact anomalies or opportunities.
"""

def explain_pie(column: str, categories: List[str], counts: List[int]) -> str:
    total = sum(counts)
    top   = categories[0] if categories else "N/A"
    top_pct = counts[0] / total * 100 if total else 0
    return f"""🥧 PIE / DONUT CHART — {column.upper()}

WHAT THIS CHART IS:
  Each slice represents one category's share of the whole.
  Larger slice = larger proportion of all records.

YOUR DATA:
  • Total records analysed: {total:,}
  • Largest slice: "{top}" ({top_pct:.1f}%)

HOW TO READ IT:
  • A near-equal pie → balanced distribution
  • One dominant slice (> 50%) → one category controls the data
  • Many tiny slices → consider grouping into "Other"

WHY THIS MATTERS:
  Proportional thinking is natural for stakeholders.
  A pie chart instantly communicates market share,
  customer segment split, or product category mix.

⚠️  CAUTION:
  Pie charts are hard to read accurately when there are many slices
  or when values are close.  Use bar charts for precise comparisons.

SUGGESTED ACTION:
  {"Well-distributed – good representation across categories." if top_pct < 50
   else f'"{top}" dominates. Consider whether this reflects reality or a data collection bias.'}
"""

def explain_missing_data(total_missing: int, cols_missing: Dict[str, int],
                          total_rows: int) -> str:
    worst = sorted(cols_missing.items(), key=lambda x: x[1], reverse=True)[:5]
    worst_str = "\n".join(
        f"  • {c}: {v} missing ({v/total_rows*100:.1f}%)  → {_missing_severity(v/total_rows*100)}"
        for c, v in worst
    )
    overall_pct = total_missing / max(1, total_rows * max(1, len(cols_missing))) * 100
    return f"""❓ MISSING DATA CHART

WHAT THIS CHART IS:
  Each bar shows what percentage of values are MISSING
  (blank / null / NaN) for that column.
  Longer bar = more data is absent.

OVERALL:
  • Total missing cells: {total_missing:,}
  • Overall missing rate: {overall_pct:.1f}%

WORST COLUMNS:
{worst_str}

SEVERITY GUIDE:
  < 2%  ✅ Excellent – ignore or use simple fill
  2–10% ✅ Good – median / mode imputation is fine
  10–25% ⚠️ Moderate – use advanced imputation (KNN, model-based)
  25–50% ⚠️ High – consider dropping the column
  > 50%  ❌ Critical – column is mostly empty, likely unusable

WHY THIS MATTERS:
  Missing data can silently bias your analysis.
  Statistical tests and machine-learning models often fail
  or give wrong results if missing values are ignored.

SUGGESTED ACTION:
  Address columns with > 10% missing data before any modelling.
"""

def explain_summary_dashboard(numeric_cols: List[str]) -> str:
    return f"""📊 NUMERIC SUMMARY DASHBOARD

WHAT THIS CHART IS:
  Four side-by-side bar charts comparing key statistics
  across all {len(numeric_cols)} numeric columns at once:

  TOP-LEFT:    Mean – the average value for each column
  TOP-RIGHT:   Std Dev – how spread out values are (higher = more variable)
  BOTTOM-LEFT: Range – the gap between the minimum and maximum value
  BOTTOM-RIGHT:Count – how many non-empty values exist per column

HOW TO READ IT:
  • High std dev relative to mean → volatile, unpredictable column
  • Low count relative to total rows → many missing values
  • Very large range → potential outliers or data entry errors

WHY THIS MATTERS:
  You can compare multiple columns simultaneously without scrolling
  through individual statistics tables — ideal for a quick sanity-check.

SUGGESTED ACTION:
  Flag any column where the count is much lower than the total rows
  (missing data concern) or std dev is larger than the mean
  (high variability that may need normalisation).
"""


# ── master dispatcher ─────────────────────────────────────────────────────────

def generate_chart_explanations(eda_stats: Dict[str, Any],
                                 chart_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Generate plain-language explanations for every chart produced.

    Returns:
        Dict mapping chart_key → explanation string
    """
    explanations: Dict[str, str] = {}
    desc  = eda_stats.get("descriptive_stats", {})
    dist  = eda_stats.get("distribution_analysis", {})
    oinfo = eda_stats.get("outlier_analysis", {})
    cat_a = eda_stats.get("categorical_analysis", {})

    # --- Histograms ---
    for item in chart_data.get("distributions", []):
        col = item["column"]
        combined = {**desc.get(col, {}), **dist.get(col, {})}
        explanations[f"histogram_{col}"] = explain_histogram(col, combined)

    # --- KDE ---
    for item in chart_data.get("kde_plots", []):
        col = item["column"]
        combined = {**desc.get(col, {}), **dist.get(col, {})}
        explanations[f"kde_{col}"] = explain_kde(col, combined)

    # --- Scatter ---
    for item in chart_data.get("scatter_plots", []):
        x, y = item["x_column"], item["y_column"]
        explanations[f"scatter_{x}_vs_{y}"] = explain_scatter(x, y, item["correlation"])

    # --- Line ---
    for item in chart_data.get("line_charts", []):
        col = item["column"]
        explanations[f"line_{col}"] = explain_line(col)

    # --- Categorical Bar ---
    for item in chart_data.get("categorical_distributions", []):
        col = item["column"]
        n   = item.get("unique_values", cat_a.get(col, {}).get("unique_values", 0))
        top = item.get("top_category", "N/A")
        cnt = item.get("top_count", 0)
        explanations[f"catbar_{col}"] = explain_categorical_bar(col, top, cnt, n)

    # --- Box Plots ---
    for item in chart_data.get("boxplots", []):
        col  = item["column"]
        oi   = oinfo.get(col, {})
        explanations[f"boxplot_{col}"] = explain_boxplot(
            col, item["q1"], item["median"], item["q3"],
            oi.get("count", 0), oi.get("percentage", 0)
        )

    # --- Violin ---
    for item in chart_data.get("violin_plots", []):
        num_col = item.get("num_column") or item.get("column", "")
        cat_col = item.get("cat_column")
        explanations[f"violin_{num_col}"] = explain_violin(num_col, cat_col)

    # --- Correlation Heatmap ---
    if chart_data.get("correlation"):
        explanations["correlation_heatmap"] = explain_correlation_heatmap(
            eda_stats.get("strong_correlations", [])
        )

    # --- Pair Plot ---
    pp = chart_data.get("pair_plot")
    if pp:
        explanations["pair_plot"] = explain_pair_plot(pp["columns"], pp.get("hue"))

    # --- Bubble ---
    for item in chart_data.get("bubble_charts", []):
        key = f"bubble_{item['x_column']}_vs_{item['y_column']}"
        explanations[key] = explain_bubble(
            item["x_column"], item["y_column"], item["size_column"]
        )

    # --- Pie ---
    for item in chart_data.get("pie_charts", []):
        col = item["column"]
        explanations[f"pie_{col}"] = explain_pie(
            col, item.get("categories", []), item.get("counts", [])
        )

    # --- Missing Data ---
    md = chart_data.get("missing_data_heatmap")
    if md:
        explanations["missing_data"] = explain_missing_data(
            md["total_missing"],
            md.get("columns_with_missing", {}),
            eda_stats.get("shape", {}).get("rows", 1)
        )

    # --- Summary Dashboard ---
    if chart_data.get("numeric_summary_stats"):
        cols = list(desc.keys())
        explanations["summary_dashboard"] = explain_summary_dashboard(cols)

    return explanations


def generate_summary_explanation(eda_stats: Dict[str, Any]) -> str:
    shape   = eda_stats.get("shape", {})
    quality = eda_stats.get("data_quality_score", {})
    missing = eda_stats.get("missing_data_summary", {})
    n_num   = len(eda_stats.get("descriptive_stats", {}))
    n_cat   = len(eda_stats.get("categorical_analysis", {}))
    n_corr  = len(eda_stats.get("strong_correlations", []))
    n_out   = eda_stats.get("total_outliers", 0)

    return f"""📋 YOUR DATASET AT A GLANCE
═══════════════════════════════════════════

SIZE:
  • {shape.get('rows', 0):,} records  ×  {shape.get('columns', 0)} columns
  • {n_num} numeric columns, {n_cat} categorical columns

DATA QUALITY:
  • Overall score:    {quality.get('overall_score', 0):.1f} / 100  ({quality.get('interpretation', 'N/A')})
  • Completeness:     {quality.get('completeness_score', 0):.1f} / 100
  • Outlier quality:  {quality.get('outlier_quality_score', 0):.1f} / 100

MISSING DATA:
  • {missing.get('total_missing', 0):,} empty cells  ({missing.get('missing_percentage', 0):.1f}% of all data)
  • {_missing_severity(missing.get('missing_percentage', 0))}

RELATIONSHIPS:
  • {n_corr} strong correlation{"s" if n_corr != 1 else ""} found (|r| > 0.7)
  • {n_out:,} outlier{"s" if n_out != 1 else ""} detected across all numeric columns

READINESS:
  {"✅ Data is in good shape – proceed with analysis." if quality.get('overall_score', 0) >= 70
   else "⚠️ Address data quality issues before drawing conclusions."}
"""


def generate_chart_interpretation_guide() -> Dict[str, str]:
    """Return a beginner's guide for all chart types."""
    return {
        "histogram": (
            "A histogram splits your data into ranges and counts how many records fall into each. "
            "Tall bars = common values.  It answers: 'What values appear most often?'"
        ),
        "kde": (
            "A KDE (Kernel Density Estimate) is a smooth histogram.  "
            "It shows where values are concentrated without the blockiness of bars. "
            "Peaks = most frequent values."
        ),
        "scatter": (
            "A scatter plot places two variables on X and Y axes, one dot per record. "
            "A diagonal pattern = the variables move together (correlation). "
            "A random cloud = no relationship."
        ),
        "line": (
            "A line chart traces values over sequence/time.  "
            "Rising line = increasing trend.  Zigzag = high variability."
        ),
        "categorical_bar": (
            "Bar heights show how many records belong to each category. "
            "Use it to see if one group dominates or if categories are balanced."
        ),
        "boxplot": (
            "The box covers the middle 50% of values.  "
            "The line inside = median.  Dots outside = outliers. "
            "A short box = consistent data; a tall box = high variability."
        ),
        "violin": (
            "A violin is a box plot with a density curve wrapped around it. "
            "Wide sections show where most values concentrate. "
            "Multiple bumps = multiple sub-groups."
        ),
        "heatmap": (
            "Each cell shows the correlation between two columns. "
            "Dark red = strong positive link; dark blue = strong inverse link; "
            "white = no connection."
        ),
        "pair_plot": (
            "A grid of scatter plots for all pairs of numeric columns at once. "
            "Diagonal = individual distributions.  Scan the grid for diagonal patterns."
        ),
        "bubble": (
            "Like a scatter plot but bubble SIZE encodes a third numeric variable. "
            "Large bubble in top-right = high on all three dimensions."
        ),
        "pie": (
            "Each slice = one category's proportion of the total. "
            "Bigger slice = more common.  Best for 2–7 categories."
        ),
        "missing_data": (
            "Bar length shows what % of that column is empty/null. "
            "Red = critical, orange = moderate, green = acceptable."
        ),
        "summary_dashboard": (
            "Four mini-charts comparing Mean, Std Dev, Range, and Count "
            "across all numeric columns simultaneously.  Quick sanity-check view."
        ),
    }


# backwards-compatible aliases (keep old names working) ─────────────────────

def generate_all_chart_explanations(eda_stats, chart_data):
    return generate_chart_explanations(eda_stats, chart_data)

def generate_dataset_summary(eda_stats):
    return generate_summary_explanation(eda_stats)

def get_interpretation_guides():
    return generate_chart_interpretation_guide()


# ── ChartExplainer class (legacy-compatible) ─────────────────────────────────

class ChartExplainer:
    """Thin class wrapper kept for backwards compatibility."""

    def explain_distribution_chart(self, col, stats):
        return explain_histogram(col, stats)

    def explain_boxplot(self, col, stats):
        return explain_boxplot(
            col,
            stats.get("q1", 0), stats.get("median", 0), stats.get("q3", 0),
            stats.get("outlier_count", 0), stats.get("outlier_percentage", 0)
        )

    def explain_correlation_heatmap(self, correlations, total_vars):
        return explain_correlation_heatmap(correlations)

    def explain_missing_data(self, missing_summary, missing_by_column):
        rows = missing_summary.get("total_missing", 1)
        return explain_missing_data(
            missing_summary.get("total_missing", 0),
            {c: v.get("count", 0) for c, v in missing_by_column.items()},
            rows
        )

    def explain_categorical_distribution(self, col, value_dist):
        top = list(value_dist.keys())[0] if value_dist else "N/A"
        cnt = list(value_dist.values())[0] if value_dist else 0
        return explain_categorical_bar(col, top, cnt, len(value_dist))

    def generate_data_quality_explanation(self, quality):
        score = quality.get("overall_score", 0)
        label = quality.get("interpretation", "Unknown")
        return (
            f"\n  Overall Quality: {score}/100 ({label})\n"
            f"  → {'Proceed with analysis.' if score >= 70 else 'Fix data quality issues first.'}\n"
        )

    def generate_interpretation_guide(self):
        return generate_chart_interpretation_guide()

    def _interpret_skewness(self, label):
        return label

    def _interpret_correlation(self, val):
        return _corr_strength(val)

    def _outlier_recommendation(self, pct):
        return _outlier_advice(pct)

    def _missing_data_status(self, pct):
        return _missing_severity(pct)