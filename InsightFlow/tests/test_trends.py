from src.core.normalizer import normalize_frame
from src.analytics.trends import calculate_trends

def test_monthly_revenue_and_orders(frame):
    result=calculate_trends(normalize_frame(frame)); assert result['monthly_revenue']=={'2026-01':1200.0,'2026-02':200.0}; assert result['monthly_orders']=={'2026-01':1,'2026-02':1}

def test_decreasing_trend(frame): assert calculate_trends(normalize_frame(frame))['trend_direction']=='decreasing'

def test_growth(frame): assert calculate_trends(normalize_frame(frame))['revenue_growth_percent']==-83.33

def test_insufficient_history(frame):
    result=calculate_trends(normalize_frame(frame.iloc[:1])); assert result['revenue_growth_percent']==0; assert result['trend_direction']=='stable'
