def test_health(client): assert client.get('/health').json()=={'status':'ok'}
def test_run_and_overview(client):
    assert client.post('/analytics/run',json={}).status_code==200; assert client.get('/analytics/overview').status_code==200

def test_analytics_views(client):
    client.post('/analytics/run',json={}); assert client.get('/analytics/trends').status_code==200; assert client.get('/analytics/categories').status_code==200; assert client.get('/analytics/products').status_code==200; assert client.get('/analytics/regions').status_code==200; assert client.get('/analytics/channels').status_code==200

def test_customers_anomalies_insights(client):
    client.post('/analytics/run',json={}); assert client.get('/analytics/customers').status_code==200; assert client.get('/analytics/anomalies').status_code==200; assert client.get('/insights').status_code==200

def test_reports_runs_quality(client):
    client.post('/analytics/run',json={}); assert client.get('/reports/latest').status_code==200; assert client.get('/analytics/runs').status_code==200; assert client.get('/data/quality').status_code==200

def test_records(client):
    client.post('/analytics/run',json={}); assert client.get('/records').status_code==200; assert client.get('/records/1').status_code==200

def test_missing_resources_and_unsafe_path(client):
    assert client.get('/analytics/runs/nope').status_code==404; assert client.get('/records/nope').status_code==404; assert client.post('/analytics/run',json={'input_path':'../outside.csv'}).status_code==400

def test_input_validation(client): assert client.post('/analytics/run',json={'input_path':'x'*501}).status_code==422
