from src.core.normalizer import normalize_frame
from src.analytics.segmentation import segment_customers

def test_segments_have_customers(frame):
    result=segment_customers(normalize_frame(frame)); assert len(result['customers'])==2; assert sum(item['customer_count'] for item in result['summary'].values())==2

def test_segment_thresholds(frame):
    result=segment_customers(normalize_frame(frame)); assert result['thresholds']['low_value_max']==450; assert result['thresholds']['high_value_min']==950

def test_empty_segments():
    import pandas as pd
    assert segment_customers(pd.DataFrame())['summary']=={}
