import pandas as pd
import numpy as np
from typing import Dict, Any
from scipy import stats


def analyze(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Perform comprehensive EDA on a pandas DataFrame with advanced statistics.
    
    Args:
        df: pandas DataFrame to analyze
    
    Returns:
        Dictionary containing:
        - shape: (rows, columns) tuple
        - column_names: list of column names
        - dtypes: dict of column types
        - missing_values: dict of missing value counts and percentages
        - descriptive_stats: dict of stats for numeric columns
        - distribution_analysis: skewness and kurtosis
        - correlation_matrix: correlation data for numeric columns
        - outlier_analysis: detailed outlier information
        - categorical_analysis: unique values and frequencies for categorical columns
        - data_quality_score: overall data quality metric
        - sample_rows: first 5 rows as dict
    """
    try:
        result = {}
        
        # ============ BASIC STRUCTURE ============
        result['shape'] = {
            'rows': int(df.shape[0]),
            'columns': int(df.shape[1])
        }
        result['column_names'] = df.columns.tolist()
        result['dtypes'] = {col: str(dtype) for col, dtype in df.dtypes.items()}
        
        # ============ MISSING VALUES ANALYSIS ============
        missing_analysis = {}
        total_cells = df.shape[0] * df.shape[1]
        total_missing = 0
        
        for col in df.columns:
            missing_count = int(df[col].isnull().sum())
            missing_percentage = round((missing_count / df.shape[0]) * 100, 2) if df.shape[0] > 0 else 0
            total_missing += missing_count
            missing_analysis[col] = {
                'count': missing_count,
                'percentage': missing_percentage
            }
        
        result['missing_values'] = missing_analysis
        result['missing_data_summary'] = {
            'total_missing': total_missing,
            'total_cells': total_cells,
            'missing_percentage': round((total_missing / total_cells) * 100, 2) if total_cells > 0 else 0
        }
        
        # ============ NUMERIC COLUMNS ANALYSIS ============
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        descriptive_stats = {}
        distribution_analysis = {}
        
        if numeric_cols:
            for col in numeric_cols:
                col_data = df[col].dropna()
                
                if len(col_data) > 0:
                    descriptive_stats[col] = {
                        'count': int(df[col].count()),
                        'mean': float(col_data.mean()),
                        'median': float(col_data.median()),
                        'mode': float(col_data.mode()[0]) if len(col_data.mode()) > 0 else None,
                        'std': float(col_data.std()),
                        'variance': float(col_data.var()),
                        'min': float(col_data.min()),
                        'q1': float(col_data.quantile(0.25)),
                        'q3': float(col_data.quantile(0.75)),
                        'max': float(col_data.max()),
                        'range': float(col_data.max() - col_data.min()),
                        'iqr': float(col_data.quantile(0.75) - col_data.quantile(0.25))
                    }
                    
                    # Distribution analysis (skewness and kurtosis)
                    try:
                        skewness = float(stats.skew(col_data))
                        kurtosis = float(stats.kurtosis(col_data))
                        
                        # Interpret skewness
                        if abs(skewness) < 0.5:
                            skew_interpretation = "Fairly Symmetric"
                        elif skewness > 0:
                            skew_interpretation = "Right Skewed (Positive)"
                        else:
                            skew_interpretation = "Left Skewed (Negative)"
                        
                        # Interpret kurtosis
                        if abs(kurtosis) < 0.5:
                            kurt_interpretation = "Similar to Normal"
                        elif kurtosis > 0:
                            kurt_interpretation = "Heavy Tails (Leptokurtic)"
                        else:
                            kurt_interpretation = "Light Tails (Platykurtic)"
                        
                        distribution_analysis[col] = {
                            'skewness': skewness,
                            'skewness_interpretation': skew_interpretation,
                            'kurtosis': kurtosis,
                            'kurtosis_interpretation': kurt_interpretation
                        }
                    except Exception as e:
                        distribution_analysis[col] = {
                            'skewness': None,
                            'skewness_interpretation': 'N/A',
                            'kurtosis': None,
                            'kurtosis_interpretation': 'N/A'
                        }
        
        result['descriptive_stats'] = descriptive_stats
        result['distribution_analysis'] = distribution_analysis
        
        # ============ CORRELATION MATRIX ============
        if len(numeric_cols) >= 2:
            corr_matrix = df[numeric_cols].corr().to_dict()
            result['correlation_matrix'] = corr_matrix
            
            # Find strong correlations
            strong_correlations = []
            for i, col1 in enumerate(numeric_cols):
                for col2 in numeric_cols[i+1:]:
                    corr_value = df[col1].corr(df[col2])
                    if abs(corr_value) > 0.7:  # Strong correlation threshold
                        strong_correlations.append({
                            'variable1': col1,
                            'variable2': col2,
                            'correlation': round(corr_value, 4)
                        })
            
            result['strong_correlations'] = strong_correlations
        else:
            result['correlation_matrix'] = None
            result['strong_correlations'] = []
        
        # ============ OUTLIER DETECTION (IQR Method) ============
        outlier_analysis = {}
        total_outliers = 0
        
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
            outlier_count = int(outlier_mask.sum())
            outlier_percentage = round((outlier_count / df.shape[0]) * 100, 2) if df.shape[0] > 0 else 0
            
            total_outliers += outlier_count
            
            outlier_analysis[col] = {
                'count': outlier_count,
                'percentage': outlier_percentage,
                'lower_bound': float(lower_bound),
                'upper_bound': float(upper_bound),
                'outlier_values': df[outlier_mask][col].tolist()[:10]  # First 10 outliers
            }
        
        result['outlier_analysis'] = outlier_analysis
        result['total_outliers'] = total_outliers
        
        # ============ CATEGORICAL ANALYSIS ============
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        categorical_analysis = {}
        
        for col in categorical_cols:
            value_counts = df[col].value_counts()
            unique_count = df[col].nunique()
            
            categorical_analysis[col] = {
                'unique_values': int(unique_count),
                'top_value': str(value_counts.index[0]) if len(value_counts) > 0 else None,
                'top_value_count': int(value_counts.values[0]) if len(value_counts) > 0 else 0,
                'value_distribution': value_counts.head(10).to_dict()
            }
        
        result['categorical_analysis'] = categorical_analysis
        
        # ============ DATA QUALITY SCORE ============
        missing_score = max(0, 100 - result['missing_data_summary']['missing_percentage'])
        completeness_score = missing_score
        
        # Outlier ratio impact on quality
        outlier_ratio = (total_outliers / max(1, df.shape[0])) * 100
        outlier_score = max(0, 100 - min(outlier_ratio * 2, 50))  # Cap impact at 50%
        
        # Overall data quality (weighted average)
        data_quality_score = round((completeness_score * 0.6 + outlier_score * 0.4), 2)
        
        result['data_quality_score'] = {
            'overall_score': data_quality_score,
            'completeness_score': round(completeness_score, 2),
            'outlier_quality_score': round(outlier_score, 2),
            'interpretation': (
                'Excellent' if data_quality_score >= 80 else
                'Good' if data_quality_score >= 60 else
                'Fair' if data_quality_score >= 40 else
                'Poor'
            )
        }
        
        # ============ SAMPLE ROWS ============
        result['sample_rows'] = df.head(5).to_dict(orient='records')
        
        # ============ CLEAN NaN VALUES ============
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