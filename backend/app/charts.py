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
        'boxplots': [],
        'pairplot': None,
        'violinplots': [],
        'missingness': None,
        'categorical_bars': []
    }
    
    try:
        # Select numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_cols:
            return result
        
        # Set seaborn style for better looking plots
        sns.set_style("whitegrid")
        
        # Decide how many columns to visualize
        max_cols = min(6, len(numeric_cols))

        # Generate distribution histograms for up to first `max_cols` numeric columns
        for col in numeric_cols[:max_cols]:
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
        for col in numeric_cols[:max_cols]:
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
        
        # Pairplot (scatter matrix) for up to 5 numeric cols (pairplot can be heavy)
        try:
            pp_cols = numeric_cols[:5]
            if len(pp_cols) >= 2:
                pair_fig = sns.pairplot(df[pp_cols].dropna(), kind='scatter', diag_kind='hist', plot_kws={'s': 15, 'alpha': 0.6})
                pair_fig.fig.suptitle('Pairwise Scatterplots', fontsize=14)
                img_bytes = io.BytesIO()
                pair_fig.fig.tight_layout()
                pair_fig.fig.savefig(img_bytes, format='png', dpi=120, bbox_inches='tight')
                img_bytes.seek(0)
                result['pairplot'] = base64.b64encode(img_bytes.read()).decode('utf-8')
                plt.close('all')
        except Exception as e:
            print(f"Error generating pairplot: {str(e)}")

        # Violin plots for distributions
        for col in numeric_cols[:max_cols]:
            try:
                fig, ax = plt.subplots(figsize=(6, 4), dpi=120)
                sns.violinplot(y=df[col].dropna(), inner='quartile', ax=ax)
                ax.set_title(f'Violin Plot of {col}', fontsize=12, fontweight='bold')
                plt.tight_layout()
                img_bytes = io.BytesIO()
                plt.savefig(img_bytes, format='png', dpi=120, bbox_inches='tight')
                img_bytes.seek(0)
                result['violinplots'].append({'column': col, 'image': base64.b64encode(img_bytes.read()).decode('utf-8')})
                plt.close(fig)
            except Exception as e:
                print(f"Error generating violin plot for {col}: {str(e)}")
                continue

        # Missingness heatmap
        try:
            fig, ax = plt.subplots(figsize=(10, 4), dpi=120)
            sns.heatmap(df.isnull(), cbar=False, cmap=['#ffffff', '#c94c4c'], ax=ax)
            ax.set_title('Missing Values Heatmap', fontsize=14, fontweight='bold')
            plt.tight_layout()
            img_bytes = io.BytesIO()
            plt.savefig(img_bytes, format='png', dpi=120, bbox_inches='tight')
            img_bytes.seek(0)
            result['missingness'] = base64.b64encode(img_bytes.read()).decode('utf-8')
            plt.close(fig)
        except Exception as e:
            print(f"Error generating missingness heatmap: {str(e)}")

        # Categorical bar charts for up to 3 categorical columns with low cardinality
        try:
            cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
            # pick categorical cols with <= 20 unique values
            small_cat = [c for c in cat_cols if df[c].nunique() <= 20][:3]
            for col in small_cat:
                try:
                    fig, ax = plt.subplots(figsize=(8, 4), dpi=120)
                    counts = df[col].value_counts().head(10)
                    sns.barplot(x=counts.values, y=counts.index, palette='muted', ax=ax)
                    ax.set_title(f'Top categories for {col}', fontsize=12, fontweight='bold')
                    ax.set_xlabel('Count')
                    plt.tight_layout()
                    img_bytes = io.BytesIO()
                    plt.savefig(img_bytes, format='png', dpi=120, bbox_inches='tight')
                    img_bytes.seek(0)
                    result['categorical_bars'].append({'column': col, 'image': base64.b64encode(img_bytes.read()).decode('utf-8')})
                    plt.close(fig)
                except Exception as e:
                    print(f"Error generating categorical bar for {col}: {str(e)}")
                    continue
        except Exception as e:
            print(f"Error selecting categorical columns: {str(e)}")

        return result
    
    except Exception as e:
        print(f"Error in generate_charts: {str(e)}")
        return result
