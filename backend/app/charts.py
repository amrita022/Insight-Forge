import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from typing import Dict, Any


def generate_charts(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Generate comprehensive charts from the DataFrame and return as base64 encoded PNG strings.
    
    Args:
        df: pandas DataFrame to visualize
    
    Returns:
        Dictionary with keys:
        - distributions: list of histogram images
        - correlation: correlation heatmap
        - boxplots: list of box plot images
        - missing_data_heatmap: visualization of missing data
        - numeric_summary_stats: statistical summary charts
        - categorical_distributions: charts for categorical variables
    """
    result = {
        'distributions': [],
        'correlation': None,
        'boxplots': [],
        'missing_data_heatmap': None,
        'numeric_summary_stats': [],
        'categorical_distributions': []
    }
    
    try:
        # Set seaborn style for better looking plots
        sns.set_style("whitegrid")
        
        # Select numeric and categorical columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        # ============ 1. DISTRIBUTION HISTOGRAMS (Numeric Columns) ============
        for col in numeric_cols[:5]:  # Extended to 5 instead of 3
            try:
                fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
                
                # Create histogram with KDE overlay
                df[col].hist(bins=30, edgecolor='black', ax=ax, alpha=0.7, color='steelblue')
                ax.axvline(df[col].mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: {df[col].mean():.2f}')
                ax.axvline(df[col].median(), color='green', linestyle='--', linewidth=2, label=f'Median: {df[col].median():.2f}')
                
                ax.set_title(f'Distribution of {col}', fontsize=14, fontweight='bold')
                ax.set_xlabel(col, fontsize=12)
                ax.set_ylabel('Frequency', fontsize=12)
                ax.legend()
                ax.grid(alpha=0.3)
                plt.tight_layout()
                
                # Convert to base64
                img_bytes = io.BytesIO()
                plt.savefig(img_bytes, format='png', dpi=120, bbox_inches='tight')
                img_bytes.seek(0)
                img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
                
                result['distributions'].append({
                    'column': col,
                    'image': img_base64,
                    'type': 'histogram',
                    'mean': float(df[col].mean()),
                    'median': float(df[col].median()),
                    'std': float(df[col].std())
                })
                plt.close(fig)
            except Exception as e:
                print(f"Error generating distribution for {col}: {str(e)}")
                continue
        
        # ============ 2. CORRELATION HEATMAP ============
        if len(numeric_cols) >= 2:
            try:
                corr_matrix = df[numeric_cols].corr()
                fig, ax = plt.subplots(figsize=(12, 10), dpi=120)
                
                sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                           center=0, square=True, ax=ax, cbar_kws={'label': 'Correlation Coefficient'},
                           vmin=-1, vmax=1, linewidths=1, linecolor='gray')
                
                ax.set_title('Correlation Matrix - Relationship Between Variables', 
                           fontsize=14, fontweight='bold')
                plt.tight_layout()
                
                # Convert to base64
                img_bytes = io.BytesIO()
                plt.savefig(img_bytes, format='png', dpi=120, bbox_inches='tight')
                img_bytes.seek(0)
                result['correlation'] = {
                    'image': base64.b64encode(img_bytes.read()).decode('utf-8'),
                    'type': 'heatmap',
                    'columns': numeric_cols
                }
                plt.close(fig)
            except Exception as e:
                print(f"Error generating correlation heatmap: {str(e)}")
        
        # ============ 3. BOXPLOTS FOR OUTLIER DETECTION ============
        for col in numeric_cols[:5]:  # Extended to 5
            try:
                fig, ax = plt.subplots(figsize=(10, 6), dpi=120)
                bp = ax.boxplot(df[col].dropna(), vert=True, patch_artist=True, widths=0.5)
                
                # Color the box
                for patch in bp['boxes']:
                    patch.set_facecolor('lightblue')
                    patch.set_alpha(0.7)
                
                for whisker in bp['whiskers']:
                    whisker.set(linewidth=2, color='darkblue')
                
                for cap in bp['caps']:
                    cap.set(linewidth=2, color='darkblue')
                
                for median in bp['medians']:
                    median.set(linewidth=2.5, color='red')
                
                ax.set_title(f'Box Plot of {col} - Outliers & Distribution', 
                           fontsize=14, fontweight='bold')
                ax.set_ylabel(col, fontsize=12)
                ax.grid(axis='y', alpha=0.3)
                
                # Add text with statistics
                q1 = df[col].quantile(0.25)
                median = df[col].median()
                q3 = df[col].quantile(0.75)
                ax.text(1.15, q1, f'Q1: {q1:.2f}', fontsize=10)
                ax.text(1.15, median, f'Median: {median:.2f}', fontsize=10, color='red')
                ax.text(1.15, q3, f'Q3: {q3:.2f}', fontsize=10)
                
                plt.tight_layout()
                
                # Convert to base64
                img_bytes = io.BytesIO()
                plt.savefig(img_bytes, format='png', dpi=120, bbox_inches='tight')
                img_bytes.seek(0)
                img_base64 = base64.b64encode(img_bytes.read()).decode('utf-8')
                
                result['boxplots'].append({
                    'column': col,
                    'image': img_base64,
                    'type': 'boxplot',
                    'q1': float(q1),
                    'median': float(median),
                    'q3': float(q3)
                })
                plt.close(fig)
            except Exception as e:
                print(f"Error generating box plot for {col}: {str(e)}")
                continue
        
        # ============ 4. MISSING DATA VISUALIZATION ============
        try:
            missing_data = df.isnull().sum()
            if missing_data.sum() > 0:
                fig, ax = plt.subplots(figsize=(12, 6), dpi=120)
                
                missing_data.plot(kind='barh', ax=ax, color='coral')
                ax.set_title('Missing Data Count by Column', fontsize=14, fontweight='bold')
                ax.set_xlabel('Number of Missing Values', fontsize=12)
                ax.grid(axis='x', alpha=0.3)
                
                plt.tight_layout()
                
                # Convert to base64
                img_bytes = io.BytesIO()
                plt.savefig(img_bytes, format='png', dpi=120, bbox_inches='tight')
                img_bytes.seek(0)
                result['missing_data_heatmap'] = {
                    'image': base64.b64encode(img_bytes.read()).decode('utf-8'),
                    'type': 'missing_data_chart',
                    'total_missing': int(missing_data.sum()),
                    'columns_with_missing': missing_data[missing_data > 0].to_dict()
                }
                plt.close(fig)
        except Exception as e:
            print(f"Error generating missing data visualization: {str(e)}")
        
        # ============ 5. CATEGORICAL DISTRIBUTIONS ============
        for col in categorical_cols[:4]:  # Top 4 categorical columns
            try:
                fig, ax = plt.subplots(figsize=(12, 6), dpi=120)
                
                value_counts = df[col].value_counts().head(15)  # Top 15 categories
                value_counts.plot(kind='barh', ax=ax, color='teal')
                
                ax.set_title(f'Distribution of {col}', fontsize=14, fontweight='bold')
                ax.set_xlabel('Count', fontsize=12)
                ax.grid(axis='x', alpha=0.3)
                
                plt.tight_layout()
                
                # Convert to base64
                img_bytes = io.BytesIO()
                plt.savefig(img_bytes, format='png', dpi=120, bbox_inches='tight')
                img_bytes.seek(0)
                
                result['categorical_distributions'].append({
                    'column': col,
                    'image': base64.b64encode(img_bytes.read()).decode('utf-8'),
                    'type': 'categorical_bar',
                    'unique_values': int(df[col].nunique()),
                    'top_category': str(value_counts.index[0]) if len(value_counts) > 0 else 'N/A'
                })
                plt.close(fig)
            except Exception as e:
                print(f"Error generating categorical chart for {col}: {str(e)}")
                continue
        
        # ============ 6. NUMERIC SUMMARY STATISTICS VISUALIZATION ============
        if numeric_cols:
            try:
                fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=120)
                
                # Mean comparison
                means = [df[col].mean() for col in numeric_cols[:8]]
                axes[0, 0].barh(numeric_cols[:8], means, color='skyblue')
                axes[0, 0].set_title('Mean Values by Column', fontweight='bold')
                axes[0, 0].grid(axis='x', alpha=0.3)
                
                # Std Dev comparison
                stds = [df[col].std() for col in numeric_cols[:8]]
                axes[0, 1].barh(numeric_cols[:8], stds, color='lightcoral')
                axes[0, 1].set_title('Standard Deviation by Column', fontweight='bold')
                axes[0, 1].grid(axis='x', alpha=0.3)
                
                # Min-Max range
                ranges = [df[col].max() - df[col].min() for col in numeric_cols[:8]]
                axes[1, 0].barh(numeric_cols[:8], ranges, color='lightgreen')
                axes[1, 0].set_title('Data Range (Max - Min) by Column', fontweight='bold')
                axes[1, 0].grid(axis='x', alpha=0.3)
                
                # Count of non-null values
                counts = [df[col].count() for col in numeric_cols[:8]]
                axes[1, 1].barh(numeric_cols[:8], counts, color='plum')
                axes[1, 1].set_title('Data Completeness by Column', fontweight='bold')
                axes[1, 1].grid(axis='x', alpha=0.3)
                
                plt.tight_layout()
                
                # Convert to base64
                img_bytes = io.BytesIO()
                plt.savefig(img_bytes, format='png', dpi=120, bbox_inches='tight')
                img_bytes.seek(0)
                
                result['numeric_summary_stats'] = {
                    'image': base64.b64encode(img_bytes.read()).decode('utf-8'),
                    'type': 'summary_stats'
                }
                plt.close(fig)
            except Exception as e:
                print(f"Error generating summary statistics: {str(e)}")
        
        return result
    
    except Exception as e:
        print(f"Error in generate_charts: {str(e)}")
        return result