from src.core.analytics_engine import analyze
from src.core.normalizer import normalize_frame

def test_engine_combines_sections(frame):
    result=analyze(normalize_frame(frame)); assert {'kpis','trends','comparison','categories','products','regions','channels','customers','anomalies'} <= result.keys()

def test_breakdown_ranks_categories(frame):
    result=analyze(normalize_frame(frame)); assert result['categories']['top']['category']=='Software'; assert result['categories']['items'][0]['revenue_share_percent'] > 0

def test_all_breakdowns_have_items(frame):
    result=analyze(normalize_frame(frame)); assert result['products']['items']; assert result['regions']['items']; assert result['channels']['items']

def test_engine_empty():
    import pandas as pd
    result=analyze(pd.DataFrame()); assert result['kpis']['total_orders']==0; assert result['anomalies']==[]
