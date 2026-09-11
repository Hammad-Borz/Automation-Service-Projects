from src.core.normalizer import normalize_frame
from src.analytics.kpis import calculate_kpis

def test_kpi_revenue_and_orders(frame):
    result=calculate_kpis(normalize_frame(frame)); assert result['total_revenue']==1400; assert result['total_orders']==2; assert result['completed_orders']==2

def test_kpi_aov_units_customers(frame):
    result=calculate_kpis(normalize_frame(frame)); assert result['average_order_value']==700; assert result['total_units_sold']==3; assert result['unique_customers']==2

def test_rates(frame):
    result=calculate_kpis(normalize_frame(frame)); assert result['completion_rate']==100; assert result['cancellation_rate']==0; assert result['refund_rate']==0

def test_status_counts():
    import pandas as pd
    from src.analytics.kpis import calculate_kpis
    data=pd.DataFrame({'calculated_total':[1,2,3,4],'status':['completed','pending','cancelled','refunded'],'quantity':[1,1,1,1],'customer_id':['a','b','c','d']})
    result=calculate_kpis(data); assert result['pending_orders']==1; assert result['cancelled_orders']==1; assert result['refunded_orders']==1

def test_empty_kpis():
    import pandas as pd
    assert calculate_kpis(pd.DataFrame())['total_orders']==0
