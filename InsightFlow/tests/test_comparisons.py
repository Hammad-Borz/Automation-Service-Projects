from src.core.normalizer import normalize_frame
from src.analytics.comparisons import compare_periods

def test_period_comparison(frame):
    result=compare_periods(normalize_frame(frame)); assert result['revenue']['current']==200; assert result['revenue']['previous']==1200; assert result['orders']['change']==0

def test_growth_calculation(frame): assert compare_periods(normalize_frame(frame))['revenue']['growth_percent']==-83.33

def test_single_period_safe(frame):
    one=normalize_frame(frame.iloc[:1]); assert compare_periods(one)['revenue']['previous']==0; assert compare_periods(one)['revenue']['growth_percent']==0
