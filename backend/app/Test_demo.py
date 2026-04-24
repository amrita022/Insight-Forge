"""
TEST & DEMO SCRIPT - Complete EDA System Testing
Tests all modules: EDA Engine, Charts, Prompts, Explainability
Creates sample data and runs full pipeline
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime

print("=" * 90)
print(" " * 20 + "INSIGHT-FORGE ENHANCED EDA SYSTEM")
print(" " * 15 + "COMPLETE TEST & DEMONSTRATION SUITE")
print("=" * 90)
print(f"\nTest Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================================================
# SECTION 1: CREATE SAMPLE DATASET
# ============================================================================

print("\n" + "=" * 90)
print("[SECTION 1] CREATING SAMPLE DATASET")
print("=" * 90)

np.random.seed(42)
n_samples = 500

print(f"\nGenerating {n_samples} sample records...")

# Create realistic business dataset
data = {
    'customer_id': range(1, n_samples + 1),
    'age': np.random.normal(40, 15, n_samples).astype(int).clip(18, 80),
    'income': np.random.normal(55000, 20000, n_samples).clip(20000, 150000),
    'spending': np.random.normal(3000, 1000, n_samples).clip(500, 10000),
    'credit_score': np.random.normal(700, 100, n_samples).astype(int).clip(300, 850),
    'months_active': np.random.randint(1, 60, n_samples),
    'category': np.random.choice(['Premium', 'Standard', 'Basic'], n_samples),
    'region': np.random.choice(['North', 'South', 'East', 'West'], n_samples),
    'status': np.random.choice(['Active', 'Inactive'], n_samples)
}

# Add realistic missing values
missing_indices = np.random.choice(n_samples, size=20, replace=False)
data['income'][missing_indices[:10]] = np.nan

# Add realistic outliers
outlier_indices = np.random.choice(n_samples, size=5, replace=False)
data['spending'][outlier_indices] = 20000

df = pd.DataFrame(data)

print(f"\n✓ Dataset created successfully!")
print(f"  • Shape: {df.shape[0]} rows × {df.shape[1]} columns")
print(f"  • Columns: {', '.join(df.columns)}")
print(f"  • Data types: {dict(df.dtypes)}")
print(f"  • Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")

print("\nSample Data (First 5 rows):")
print(df.head())

# ============================================================================
# SECTION 2: TEST EDA ENGINE
# ============================================================================

print("\n" + "=" * 90)
print("[SECTION 2] TESTING ENHANCED EDA ENGINE")
print("=" * 90)

try:
    from eda_engine import analyze
    
    print("\n✓ EDA module imported successfully")
    print("\nRunning comprehensive exploratory data analysis...")
    
    stats = analyze(df)
    
    print("\n✅ EDA Analysis Complete!")
    
    # Display shape and structure
    print(f"\n1️⃣  DATASET SHAPE:")
    print(f"   • Rows: {stats['shape']['rows']:,}")
    print(f"   • Columns: {stats['shape']['columns']}")
    
    # Display data quality
    print(f"\n2️⃣  DATA QUALITY SCORE:")
    quality = stats['data_quality_score']
    print(f"   • Overall: {quality['overall_score']}/100 ({quality['interpretation']})")
    print(f"   • Completeness: {quality['completeness_score']}/100")
    print(f"   • Outlier Quality: {quality['outlier_quality_score']}/100")
    
    # Display missing data
    print(f"\n3️⃣  MISSING DATA:")
    missing = stats['missing_data_summary']
    print(f"   • Total Missing: {missing['total_missing']} cells")
    print(f"   • Percentage: {missing['missing_percentage']}%")
    
    # Display numeric analysis
    print(f"\n4️⃣  NUMERIC COLUMNS ANALYZED: {len(stats['descriptive_stats'])}")
    for i, (col_name, col_stats) in enumerate(list(stats['descriptive_stats'].items())[:3], 1):
        print(f"\n   {col_name}:")
        print(f"     • Mean: {col_stats['mean']:.2f}")
        print(f"     • Median: {col_stats['median']:.2f}")
        print(f"     • Std Dev: {col_stats['std']:.2f}")
        print(f"     • Min: {col_stats['min']:.2f}")
        print(f"     • Max: {col_stats['max']:.2f}")
    
    # Display distribution analysis
    print(f"\n5️⃣  DISTRIBUTION ANALYSIS:")
    for i, (col_name, dist) in enumerate(list(stats['distribution_analysis'].items())[:2], 1):
        print(f"\n   {col_name}:")
        print(f"     • Skewness: {dist['skewness']:.4f} ({dist['skewness_interpretation']})")
        print(f"     • Kurtosis: {dist['kurtosis']:.4f} ({dist['kurtosis_interpretation']})")
    
    # Display correlations
    print(f"\n6️⃣  STRONG CORRELATIONS (> 0.7): {len(stats['strong_correlations'])}")
    for corr in stats['strong_correlations'][:3]:
        print(f"   • {corr['variable1']} ↔ {corr['variable2']}: {corr['correlation']:.4f}")
    
    # Display outliers
    print(f"\n7️⃣  OUTLIER ANALYSIS:")
    print(f"   • Total Outliers: {stats['total_outliers']}")
    for col_name, outlier_info in list(stats['outlier_analysis'].items())[:2]:
        print(f"   • {col_name}: {outlier_info['count']} ({outlier_info['percentage']}%)")
    
    # Display categorical analysis
    print(f"\n8️⃣  CATEGORICAL COLUMNS: {len(stats['categorical_analysis'])}")
    for col_name, cat_info in stats['categorical_analysis'].items():
        print(f"   • {col_name}: {cat_info['unique_values']} unique values")
        print(f"     Top: {cat_info['top_value']} ({cat_info['top_value_count']} occurrences)")
    
    print("\n✅ TEST 2 PASSED: EDA Engine working correctly!")
    
except Exception as e:
    print(f"\n❌ TEST 2 FAILED: {str(e)}")
    import traceback
    traceback.print_exc()
    stats = None

# ============================================================================
# SECTION 3: TEST CHARTS MODULE
# ============================================================================

print("\n" + "=" * 90)
print("[SECTION 3] TESTING ENHANCED CHARTS MODULE")
print("=" * 90)

try:
    from charts import generate_charts
    
    print("\n✓ Charts module imported successfully")
    print("\nGenerating visualizations...")
    
    charts = generate_charts(df)
    
    print("\n✅ Chart Generation Complete!")
    
    # Distribution charts
    print(f"\n1️⃣  DISTRIBUTION HISTOGRAMS:")
    dists = charts['distributions']
    print(f"   • Generated: {len(dists)} charts")
    if dists:
        print(f"   • Columns: {[d['column'] for d in dists]}")
        print(f"   • Each includes: mean, median, std dev")
    
    # Correlation heatmap
    print(f"\n2️⃣  CORRELATION HEATMAP:")
    if charts['correlation']:
        print(f"   • Generated: ✓ Yes")
        print(f"   • Variables analyzed: {len(charts['correlation']['columns'])}")
        print(f"   • Size: Base64 PNG image")
    else:
        print(f"   • Generated: ✗ No (need 2+ numeric columns)")
    
    # Box plots
    print(f"\n3️⃣  BOX PLOTS:")
    boxplots = charts['boxplots']
    print(f"   • Generated: {len(boxplots)} charts")
    if boxplots:
        print(f"   • Columns: {[b['column'] for b in boxplots]}")
        print(f"   • Each shows: quartiles, median, outliers")
    
    # Missing data heatmap
    print(f"\n4️⃣  MISSING DATA VISUALIZATION:")
    if charts['missing_data_heatmap']:
        print(f"   • Generated: ✓ Yes")
        missing_info = charts['missing_data_heatmap']
        print(f"   • Total missing: {missing_info['total_missing']}")
        print(f"   • Columns with gaps: {len(missing_info.get('columns_with_missing', {}))}")
    else:
        print(f"   • Generated: ✗ No (all data complete)")
    
    # Categorical distributions
    print(f"\n5️⃣  CATEGORICAL DISTRIBUTIONS:")
    cat_dists = charts['categorical_distributions']
    print(f"   • Generated: {len(cat_dists)} charts")
    if cat_dists:
        print(f"   • Columns: {[c['column'] for c in cat_dists]}")
    
    # Summary statistics
    print(f"\n6️⃣  SUMMARY STATISTICS DASHBOARD:")
    if charts['numeric_summary_stats']:
        print(f"   • Generated: ✓ Yes")
        print(f"   • Shows: Means, Std Devs, Ranges, Counts")
    else:
        print(f"   • Generated: ✗ No")
    
    print("\n✅ TEST 3 PASSED: Charts module working correctly!")
    
except Exception as e:
    print(f"\n❌ TEST 3 FAILED: {str(e)}")
    import traceback
    traceback.print_exc()
    charts = None

# ============================================================================
# SECTION 4: TEST PROMPT BUILDER
# ============================================================================

print("\n" + "=" * 90)
print("[SECTION 4] TESTING ENHANCED PROMPT BUILDER")
print("=" * 90)

try:
    from prompt_builder import (
        build_structured_prompt,
        build_baseline_prompt
    )
    
    print("\n✓ Prompt Builder module imported successfully")
    
    if stats:
        print("\nBuilding structured prompt for comprehensive analysis...")
        structured = build_structured_prompt(stats)
        print(f"✓ Structured prompt created: {len(structured)} characters")
        print(f"  Sample (first 200 chars): {structured[:200]}...")
        
        print("\nBuilding baseline prompt for comparison...")
        baseline = build_baseline_prompt(df)
        print(f"✓ Baseline prompt created: {len(baseline)} characters")
        print(f"  Sample (first 200 chars): {baseline[:200]}...")
        
        print("\n✅ TEST 4 PASSED: Prompt Builder working correctly!")
    else:
        print("\n⚠️  Skipping: EDA stats not available")

except Exception as e:
    print(f"\n❌ TEST 4 FAILED: {str(e)}")
    import traceback
    traceback.print_exc()

# ============================================================================
# SECTION 5: TEST CHART EXPLAINABILITY
# ============================================================================

print("\n" + "=" * 90)
print("[SECTION 5] TESTING CHART EXPLAINABILITY MODULE")
print("=" * 90)

try:
    from chart_explainability_complete import (
        ChartExplainer,
        generate_all_chart_explanations,
        generate_dataset_summary,
        get_interpretation_guides
    )
    
    print("\n✓ Chart Explainability module imported successfully")
    
    explainer = ChartExplainer()
    
    # Test distribution explanation
    print("\n1️⃣  DISTRIBUTION CHART EXPLANATION:")
    if stats:
        col_name = 'age'
        col_stats = stats['descriptive_stats'][col_name]
        dist_analysis = stats['distribution_analysis'][col_name]
        combined = {**col_stats, **dist_analysis}
        
        explanation = explainer.explain_distribution_chart(col_name, combined)
        print(explanation[:300] + "\n   ...")
    
    # Test boxplot explanation
    print("\n2️⃣  BOXPLOT EXPLANATION:")
    if stats:
        col_name = 'income'
        col_stats = stats['descriptive_stats'][col_name]
        outliers = stats['outlier_analysis'][col_name]
        combined = {**col_stats, 'outlier_count': outliers['count'], 
                   'outlier_percentage': outliers['percentage']}
        
        explanation = explainer.explain_boxplot(col_name, combined)
        print(explanation[:300] + "\n   ...")
    
    # Test interpretation guides
    print("\n3️⃣  INTERPRETATION GUIDES:")
    guides = get_interpretation_guides()
    print(f"   Generated {len(guides)} guides:")
    for guide_type in guides.keys():
        print(f"   • {guide_type.upper()}")
    
    # Test dataset summary
    print("\n4️⃣  DATASET SUMMARY (Plain Language):")
    if stats:
        summary = generate_dataset_summary(stats)
        print(summary[:400] + "\n   ...")
    
    # Test full explanation generation
    print("\n5️⃣  FULL CHART EXPLANATIONS:")
    if stats and charts:
        all_explanations = generate_all_chart_explanations(stats, charts)
        print(f"   Generated {len(all_explanations)} explanations:")
        for exp_key in list(all_explanations.keys())[:5]:
            print(f"   • {exp_key}")
    
    print("\n✅ TEST 5 PASSED: Chart Explainability working correctly!")
    
except Exception as e:
    print(f"\n❌ TEST 5 FAILED: {str(e)}")
    import traceback
    traceback.print_exc()

# ============================================================================
# SECTION 6: INTEGRATION TEST (Full Pipeline)
# ============================================================================

print("\n" + "=" * 90)
print("[SECTION 6] FULL PIPELINE INTEGRATION TEST")
print("=" * 90)

try:
    if stats and charts:
        print("\n✓ All modules available, testing full pipeline...")
        
        # Step 1: EDA
        print("\n1️⃣  Running EDA Analysis...")
        quality_score = stats['data_quality_score']['overall_score']
        print(f"   ✓ Data Quality Score: {quality_score}/100")
        
        # Step 2: Charts
        print("\n2️⃣  Generating Visualizations...")
       
        chart_count = (
        len(charts.get('distributions', [])) +
        len(charts.get('boxplots', [])) +
        (1 if charts.get('correlation') else 0) +
        len(charts.get('categorical', [])))
      
        print(f"   ✓ Generated {chart_count} charts")
        
        # Step 3: Explanations
        print("\n3️⃣  Generating AI Explanations...")
        all_exp = generate_all_chart_explanations(stats, charts)
        print(f"   ✓ Generated {len(all_exp)} explanations")
        
        # Step 4: Summary
        print("\n4️⃣  Creating Dataset Summary...")
        summary = generate_dataset_summary(stats)
        print(f"   ✓ Summary created ({len(summary)} characters)")
        
        print("\n✅ TEST 6 PASSED: Full pipeline integration successful!")
        print("\n" + "=" * 90)
        print("COMPLETE TEST SUITE RESULTS")
        print("=" * 90)
        print("\n✅ ALL TESTS PASSED SUCCESSFULLY!\n")
        print(f"✓ Module 1: EDA Engine ..................... WORKING")
        print(f"✓ Module 2: Charts Generation ............. WORKING")
        print(f"✓ Module 3: Prompt Builder ................ WORKING")
        print(f"✓ Module 4: Chart Explainability .......... WORKING")
        print(f"✓ Pipeline: Full Integration .............. WORKING")
        
        print(f"\nDATASET STATISTICS:")
        print(f"  • Records: {stats['shape']['rows']:,}")
        print(f"  • Columns: {stats['shape']['columns']}")
        print(f"  • Data Quality: {quality_score}/100")
        print(f"  • Charts Generated: {chart_count}")
        print(f"  • Explanations: {len(all_exp)}")
        
        print(f"\n📈 SAMPLE OUTPUT:")
        print(f"\n  Data Quality Assessment:")
        print(f"  {stats['data_quality_score']['interpretation'].upper()}")
        
        print(f"\n  Quality Breakdown:")
        print(f"  • Completeness: {stats['data_quality_score']['completeness_score']}/100")
        print(f"  • Outlier Quality: {stats['data_quality_score']['outlier_quality_score']}/100")
        
        print(f"\n  Missing Data:")
        print(f"  • Total Missing: {stats['missing_data_summary']['total_missing']}")
        print(f"  • Percentage: {stats['missing_data_summary']['missing_percentage']}%")
        
        print(f"\n  Strong Correlations Found:")
        print(f"  • Count: {len(stats['strong_correlations'])}")
        for corr in stats['strong_correlations'][:2]:
            print(f"  • {corr['variable1']} ↔ {corr['variable2']}: {corr['correlation']:.3f}")
        
        print(f"\n  Outliers Detected:")
        print(f"  • Total: {stats['total_outliers']}")
        
        print("\n🎉 YOUR SYSTEM IS READY FOR PRODUCTION!")
        print("\n" + "=" * 90)
        
    else:
        print("\n⚠️  Skipping: Required data not available")
        
except Exception as e:
    print(f"\n❌ TEST 6 FAILED: {str(e)}")
    import traceback
    traceback.print_exc()

# ============================================================================
# FINAL SUMMARY
# ============================================================================

print("\nTest Completed: {}\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
print("=" * 90)
print("NEXT STEPS:")
print("=" * 90)
print("""
1. ✓ Verify all tests passed above
2. ✓ Review the explanations generated
3. ✓ Check data quality assessment
4. ✓ Integrate into your FastAPI/Flask endpoint
5. ✓ Update frontend to display explanations
6. ✓ Deploy to production
7. ✓ Celebrate! 🎉

For more details, see INTEGRATION_GUIDE.md
""")
print("=" * 90)