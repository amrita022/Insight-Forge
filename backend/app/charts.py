import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from typing import Dict, Any


def generate_charts(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate charts from the DataFrame and return as base64 encoded PNG strings.
    
    Args:
        df: pandas DataFrame to visualize
    
    Returns:
        Dictionary with keys:
        - distributions: list of base64 encoded histogram images
        - correlation: base64 encoded correlation heatmap (or None)
        - boxplots: list of base64 encoded box plot images
    """
    result = {
        'distributions': [],
        'correlation': None,
        'boxplots': []
    }
    
    try:
        # Select numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_cols:
            return result
        
        # Set seaborn style for better looking plots
        sns.set_style("whitegrid")
        
        # Generate distribution histograms for first 3 numeric columns
        for col in numeric_cols[:3]:
            try:
                fig, ax = plt.subplots(figsize=(8, 5), dpi=120)
                df[col].hist(bins=30, edgecolor='black', ax=ax)
                ax.set_title(f'Distribution of {col}', fontsize=14, fontweight='bold')
                ax.set_xlabel(col, fontsize=12)
                ax.set_ylabel('Frequency', fontsize=12)
                plt.tight_layout()
                
                # Convert to base64
                img_bytes = io.BytesIO()
                plt.savefig(img_bytes, format='png', dpi=120, bbox_inches='tight')
                img_bytes.seek(0)
                img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
                result['distributions'].append({
                    'column': col,
                    'image': img_base64
                })
                plt.close(fig)
            except Exception as e:
                print(f"Error generating distribution for {col}: {str(e)}")
                continue
        
        # Generate correlation heatmap if 2+ numeric columns
        if len(numeric_cols) >= 2:
            try:
                corr_matrix = df[numeric_cols].corr()
                fig, ax = plt.subplots(figsize=(10, 8), dpi=120)
                sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                           center=0, square=True, ax=ax, cbar_kws={'label': 'Correlation'})
                ax.set_title('Correlation Matrix', fontsize=14, fontweight='bold')
                plt.tight_layout()
                
                # Convert to base64
                img_bytes = io.BytesIO()
                plt.savefig(img_bytes, format='png', dpi=120, bbox_inches='tight')
                img_bytes.seek(0)
                result['correlation'] = base64.b64encode(img_bytes.read()).decode('utf-8')
                plt.close(fig)
            except Exception as e:
                print(f"Error generating correlation heatmap: {str(e)}")
        
        # Generate box plots for outlier visualization
        for col in numeric_cols[:3]:
            try:
                fig, ax = plt.subplots(figsize=(8, 5), dpi=120)
                bp = ax.boxplot(df[col].dropna(), vert=True, patch_artist=True)
                
                # Color the box
                for patch in bp['boxes']:
                    patch.set_facecolor('lightblue')
                
                ax.set_title(f'Box Plot of {col}', fontsize=14, fontweight='bold')
                ax.set_ylabel(col, fontsize=12)
                ax.grid(axis='y', alpha=0.3)
                plt.tight_layout()
                
                # Convert to base64
                img_bytes = io.BytesIO()
                plt.savefig(img_bytes, format='png', dpi=120, bbox_inches='tight')
                img_bytes.seek(0)
                img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
                result['boxplots'].append({
                    'column': col,
                    'image': img_base64
                })
                plt.close(fig)
            except Exception as e:
                print(f"Error generating box plot for {col}: {str(e)}")
                continue
        
        return result
    
    except Exception as e:
        print(f"Error in generate_charts: {str(e)}")
        return result
