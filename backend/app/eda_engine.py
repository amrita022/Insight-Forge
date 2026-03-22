import pandas as pd
import numpy as np
from typing import Dict, Any


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
            corr_matrix = df[numeric_cols].corr().to_dict()
            result['correlation_matrix'] = corr_matrix
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
        
        return result
    
    except Exception as e:
        raise Exception(f"Error during EDA analysis: {str(e)}")
