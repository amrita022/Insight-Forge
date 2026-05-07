import pandas as pd
from app.eda_engine import explain_pairwise_relations


def test_explain_pairwise_relations_basic():
    # create dataframe with known correlation
    df = pd.DataFrame({
        'x': [1,2,3,4,5,6,7,8,9,10],
        'y': [2,4,6,8,10,12,14,16,18,20],
        'z': [5,5,5,5,5,5,5,5,5,5]
    })

    numeric_cols = ['x','y','z']
    explanations = explain_pairwise_relations(df, numeric_cols)
    # Expect at least one explanation for x-y pair
    assert any(e['x']=='x' and e['y']=='y' for e in explanations)
    xy = next(e for e in explanations if e['x']=='x' and e['y']=='y')
    assert abs(xy['pearson_r'] - 1.0) < 1e-6
    assert xy['slope'] is not None

*** End Patch