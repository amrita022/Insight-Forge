import pandas as pd
import numpy as np
from typing import Dict, Any, List, Tuple
from math import isfinite
try:
    from scipy import stats
except Exception:
    stats = None


def analyze(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Perform comprehensive EDA on a pandas DataFrame.
    
    Args:
        df: pandas DataFrame to analyze
    
    Returns:
        Dictionary containing:
        - shape: (rows, columns) tuple
        - column_names: list of column names
        - dtypes: dict of column types
        - missing_values: dict of missing value counts
        - descriptive_stats: dict of stats for numeric columns
        - correlation_matrix: correlation data for numeric columns
        - outlier_counts: dict of outlier counts per column
        - sample_rows: first 5 rows as dict
    """
    try:
        result = {}
        
        # Basic shape and structure
        result['shape'] = {
            'rows': int(df.shape[0]),
            'columns': int(df.shape[1])
        }
        result['column_names'] = df.columns.tolist()
        result['dtypes'] = {col: str(dtype) for col, dtype in df.dtypes.items()}
        
        # Missing values
        result['missing_values'] = {
            col: int(df[col].isnull().sum()) 
            for col in df.columns
        }
        
        # Descriptive stats for numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        descriptive_stats = {}
        
        if numeric_cols:
            stats_df = df[numeric_cols].describe().to_dict()
            for col in numeric_cols:
                descriptive_stats[col] = {
                    'mean': float(df[col].mean()) if not df[col].isna().all() else None,
                    'median': float(df[col].median()) if not df[col].isna().all() else None,
                    'std': float(df[col].std()) if not df[col].isna().all() else None,
                    'min': float(df[col].min()) if not df[col].isna().all() else None,
                    'max': float(df[col].max()) if not df[col].isna().all() else None,
                    'count': int(df[col].count())
                }
        
        result['descriptive_stats'] = descriptive_stats
        
        # Correlation matrix for numeric columns
        if len(numeric_cols) >= 2:
            corr_matrix = df[numeric_cols].corr()
            result['correlation_matrix'] = corr_matrix.to_dict()
        else:
            result['correlation_matrix'] = None
        
        # Outlier detection using IQR method
        outlier_counts = {}
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            outlier_counts[col] = int(outliers)
        
        result['outlier_counts'] = outlier_counts
        
        # Sample rows (first 5)
        result['sample_rows'] = df.head(5).to_dict(orient='records')
        
        def clean_nan(obj):
            if isinstance(obj, dict):
                return {k: clean_nan(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [clean_nan(v) for v in obj]
            elif isinstance(obj, float) and (obj != obj or obj == float('inf') or obj == float('-inf')):
                return None
            return obj
        
        return clean_nan(result)
    
    except Exception as e:
        raise Exception(f"Error during EDA analysis: {str(e)}")


def explain_pairwise_relations(df: pd.DataFrame, numeric_cols: List[str]) -> List[Dict[str, Any]]:
    """
    For top correlated pairs, produce detailed explainability including
    Pearson r, p-value (if scipy available), linear fit, direction, strength,
    and suggested interpretation.
    """
    explanations = []
    if len(numeric_cols) < 2:
        return explanations

    corr = df[numeric_cols].corr()

    # Flatten pairs and sort by absolute correlation
    pairs: List[Tuple[str, str, float]] = []
    for i, col1 in enumerate(numeric_cols):
        for col2 in numeric_cols[i+1:]:
            r = corr.loc[col1, col2]
            if not isfinite(r):
                continue
            pairs.append((col1, col2, float(r)))

    pairs.sort(key=lambda x: abs(x[2]), reverse=True)

    # Generate explanations for top 5 pairs or those with |r| >= 0.25
    for col1, col2, r in pairs[:5]:
        if abs(r) < 0.25:
            # stop if correlations are weak
            break

        # compute regression slope/intercept
        try:
            clean_df = df[[col1, col2]].dropna()
            if clean_df.shape[0] < 3:
                slope = None
                intercept = None
            else:
                slope, intercept = np.polyfit(clean_df[col1], clean_df[col2], 1)
        except Exception:
            slope = None
            intercept = None

        p_value = None
        if stats is not None:
            try:
                # scipy.stats.pearsonr may fail on constant arrays
                clean = df[[col1, col2]].dropna()
                if clean.shape[0] >= 3:
                    p_value = float(stats.pearsonr(clean[col1], clean[col2])[1])
            except Exception:
                p_value = None

        strength = _interpret_correlation_strength(r)
        direction = 'positive' if r > 0 else 'negative'

        narrative = (
            f"The variables '{col1}' and '{col2}' show a {direction} relationship "
            f"(Pearson r = {r:.3f}). This indicates {strength}."
        )
        if slope is not None:
            narrative += f" A linear fit suggests that for each unit increase in '{col1}', '{col2}' changes by approximately {slope:.3f} units."
        if p_value is not None:
            narrative += f" The p-value for the correlation is {p_value:.3g}, indicating {'statistical significance' if p_value < 0.05 else 'no strong evidence of significance'} at α=0.05."

        # Enhanced layman narrative with quantitative examples
        layman_text = f"In plain terms: when {col1} goes {'up' if r>0 else 'down'}, {col2} tends to go {'up' if r>0 else 'down'} as well. "
        
        # Add quantitative example with actual values
        try:
            col1_vals = df[col1].dropna()
            col2_vals = df[col2].dropna()
            if len(col1_vals) > 0 and len(col2_vals) > 0:
                col1_q1 = col1_vals.quantile(0.25)
                col1_q3 = col1_vals.quantile(0.75)
                col2_at_q1 = df[df[col1] <= col1_q1][col2].mean()
                col2_at_q3 = df[df[col1] >= col1_q3][col2].mean()
                
                if not np.isnan(col2_at_q1) and not np.isnan(col2_at_q3) and col1_q1 != col1_q3:
                    change = col2_at_q3 - col2_at_q1
                    layman_text += (
                        f"Example: when {col1} is around {col1_q1:.2f} (lower quartile), {col2} averages {col2_at_q1:.2f}; "
                        f"when {col1} rises to {col1_q3:.2f} (upper quartile), {col2} averages {col2_at_q3:.2f}—a change of {change:+.2f}. "
                    )
        except Exception:
            pass
        
        layman_text += f"The relationship is {strength.replace('a ', '')}. This doesn't prove one causes the other, but they often move together."

        explanations.append({
            'x': col1,
            'y': col2,
            'pearson_r': float(r),
            'p_value': p_value,
            'slope': slope,
            'intercept': intercept,
            'strength': strength,
            'direction': direction,
            'narrative': narrative,
            'layman_narrative': layman_text
        })

    return explanations


def _interpret_correlation_strength(r: float) -> str:
    ar = abs(r)
    if ar >= 0.8:
        return 'a very strong relationship'
    if ar >= 0.6:
        return 'a strong relationship'
    if ar >= 0.4:
        return 'a moderate relationship'
    if ar >= 0.25:
        return 'a weak-to-moderate relationship'
    return 'a very weak or negligible relationship'


def explain_outliers(df: pd.DataFrame, numeric_cols: List[str]) -> Dict[str, Any]:
    """
    Explain outliers detected via IQR method for each numeric column.
    Returns explanation narrative for each column with outliers.
    """
    outlier_explanations = {}
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
        outlier_count = outlier_mask.sum()
        outlier_pct = (outlier_count / len(df)) * 100 if len(df) > 0 else 0
        
        if outlier_count > 0:
            outlier_values = df.loc[outlier_mask, col]
            min_outlier = outlier_values.min()
            max_outlier = outlier_values.max()
            
            narrative = (
                f"'{col}' contains {outlier_count} outlier(s) ({outlier_pct:.1f}% of data). "
                f"Using the IQR method (1.5 × IQR rule), outliers are values < {lower_bound:.2f} or > {upper_bound:.2f}. "
                f"Detected outliers range from {min_outlier:.2f} to {max_outlier:.2f}. "
                f"These may represent genuine extremes, measurement errors, or special cases worth investigating."
            )
        else:
            narrative = f"'{col}' contains no outliers detected by the IQR method, suggesting a stable distribution without extreme values."

        # Plain-language summary for non-technical users
        if outlier_count > 0:
            layman = (
                f"Plainly: {outlier_count} value(s) ({outlier_pct:.1f}% of the data) look unusual for {col}. "
                "They might be real but rare cases, or they could be data errors — check those rows."
            )
        else:
            layman = (f"Plainly: {col} looks consistent — we didn't find unusual extreme values.")

        outlier_explanations[col] = {
            'count': int(outlier_count),
            'percentage': float(outlier_pct),
            'lower_bound': float(lower_bound),
            'upper_bound': float(upper_bound),
            'narrative': narrative,
            'layman_narrative': layman
        }
    
    return outlier_explanations


def explain_distributions(df: pd.DataFrame, numeric_cols: List[str]) -> Dict[str, Any]:
    """
    Explain the distribution characteristics of numeric columns with quantitative examples.
    """
    dist_explanations = {}
    
    for col in numeric_cols:
        try:
            mean = df[col].mean()
            median = df[col].median()
            std = df[col].std()
            skewness = df[col].skew()
            min_val = df[col].min()
            max_val = df[col].max()
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            
            # Interpret skewness
            if abs(skewness) < 0.5:
                skew_desc = "approximately symmetric"
            elif skewness > 0:
                skew_desc = "right-skewed (tail on the right)"
            else:
                skew_desc = "left-skewed (tail on the left)"
            
            # Interpret spread
            range_val = max_val - min_val
            if std < range_val * 0.1:
                spread_desc = "tightly concentrated"
            else:
                spread_desc = "widely spread"
            
            # Enhanced narrative with quartile ranges
            narrative = (
                f"The distribution of '{col}' is {skew_desc} with mean={mean:.2f} and median={median:.2f}. "
                f"Values range from {min_val:.2f} to {max_val:.2f} (range: {range_val:.2f}). "
                f"The middle 50% of values (Q1 to Q3) fall between {q1:.2f} and {q3:.2f}. "
                f"Standard deviation is {std:.2f}, indicating {spread_desc} spread. "
                f"Skewness of {skewness:.3f} confirms the {skew_desc.split('(')[0].strip()} character."
            )

            # Enhanced plain-language version with examples
            iqr = q3 - q1
            layman = (
                f"Plainly: {col} typically averages around {median:.1f}. "
                f"Most cases (the middle 50%) fall between {q1:.1f} and {q3:.1f}. "
                f"Values range from as low as {min_val:.1f} to as high as {max_val:.1f}. "
                f"The typical spread (standard deviation) is {std:.1f}, so expect variation of roughly ±{std:.1f} from the average. "
                f"Data is {skew_desc.split('(')[0].strip()}—not perfectly balanced, with a tail toward the {'high' if skewness > 0 else 'low'} end."
            )

            dist_explanations[col] = {
                'mean': float(mean),
                'median': float(median),
                'std': float(std),
                'min': float(min_val),
                'max': float(max_val),
                'q1': float(q1),
                'q3': float(q3),
                'skewness': float(skewness),
                'skew_description': skew_desc,
                'narrative': narrative,
                'layman_narrative': layman
            }
        except Exception as e:
            dist_explanations[col] = {
                'narrative': f"Could not compute distribution statistics: {str(e)}"
            }
    
    return dist_explanations


def explain_correlation_matrix(df: pd.DataFrame, numeric_cols: List[str]) -> str:
    """
    Generate a narrative explanation of the overall correlation structure.
    """
    if len(numeric_cols) < 2:
        return "Insufficient numeric columns to compute correlation matrix."
    
    corr = df[numeric_cols].corr()
    
    # Find strongest correlations
    pairs = []
    for i, col1 in enumerate(numeric_cols):
        for col2 in numeric_cols[i+1:]:
            r = corr.loc[col1, col2]
            if isfinite(r):
                pairs.append((col1, col2, float(r)))
    
    pairs.sort(key=lambda x: abs(x[2]), reverse=True)
    
    # Build narrative
    strong_pairs = [p for p in pairs if abs(p[2]) >= 0.6]
    moderate_pairs = [p for p in pairs if 0.4 <= abs(p[2]) < 0.6]
    
    narrative = "Correlation Matrix Summary: "
    
    if strong_pairs:
        narrative += f"Found {len(strong_pairs)} strong relationship(s): "
        narrative += "; ".join([f"{p[0]} & {p[1]} (r={p[2]:.2f})" for p in strong_pairs[:3]])
    
    if moderate_pairs:
        narrative += f". Also found {len(moderate_pairs)} moderate relationship(s). "
    
    if not strong_pairs and not moderate_pairs:
        narrative += "Most variables show weak or negligible correlations."
    
    # Plain summary for lay users
    if strong_pairs:
        lay = f"Plainly: there are {len(strong_pairs)} strong connections between some variables, such as {strong_pairs[0][0]} and {strong_pairs[0][1]}."
    elif moderate_pairs:
        lay = "Plainly: a few variables show moderate relationships — some move together somewhat consistently."
    else:
        lay = "Plainly: variables do not show strong relationships; most behave independently."

    return {
        'narrative': narrative,
        'layman_summary': lay
    }
