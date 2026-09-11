import pandas as pd
from src.analytics.anomalies import detect_anomalies

def test_no_anomaly_with_insufficient_history():
    frame=pd.DataFrame({'order_date':pd.to_datetime(['2026-01-01','2026-01-02','2026-01-03']),'calculated_total':[1,2,3],'order_id':['1','2','3']}); assert detect_anomalies(frame)==[]

def test_spike_detection():
    dates=pd.date_range('2026-01-01',periods=6); frame=pd.DataFrame({'order_date':dates,'calculated_total':[10,10,10,10,10,100],'order_id':list('abcdef')}); result=detect_anomalies(frame,1.5); assert any(item['anomaly_type']=='spike' for item in result)

def test_drop_detection():
    dates=pd.date_range('2026-01-01',periods=6); frame=pd.DataFrame({'order_date':dates,'calculated_total':[100,100,100,100,100,1],'order_id':list('abcdef')}); assert any(item['anomaly_type']=='drop' for item in detect_anomalies(frame,1.5))

def test_anomaly_fields():
    dates=pd.date_range('2026-01-01',periods=6); frame=pd.DataFrame({'order_date':dates,'calculated_total':[10,10,10,10,10,100],'order_id':list('abcdef')}); item=detect_anomalies(frame,1.5)[0]; assert {'date','metric','value','baseline','deviation','anomaly_type','severity'} <= item.keys()
