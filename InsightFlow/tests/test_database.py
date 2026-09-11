import pandas as pd
from src.database.connection import initialize_database
from src.database.repository import AnalyticsRepository

def record(order='1', total=10):
    return pd.DataFrame([{'record_id':order,'order_id':order,'customer_id':'c','customer_name':'A','customer_email':'a@x.test','product':'P','category':'C','quantity':1,'unit_price':total,'total_amount':total,'calculated_total':total,'order_date':'2026-01-01','status':'completed','region':'East','sales_channel':'online'}])

def test_database_initialization(tmp_path):
    path=tmp_path/'x.sqlite3'; initialize_database(path); assert path.exists()

def test_insert_retrieve(tmp_path):
    repo=AnalyticsRepository(tmp_path/'x.sqlite3'); repo.upsert_records(record()); assert repo.get_record('1')['calculated_total']==10

def test_upsert_is_idempotent(tmp_path):
    repo=AnalyticsRepository(tmp_path/'x.sqlite3'); repo.upsert_records(record()); repo.upsert_records(record(total=25)); assert len(repo.list_records())==1; assert repo.get_record('1')['calculated_total']==25

def test_run_and_snapshot_persistence(tmp_path):
    repo=AnalyticsRepository(tmp_path/'x.sqlite3'); run={'run_id':'r1','started_at':'now','completed_at':'later','status':'completed','input_records':1,'valid_records':1,'invalid_records':0,'duplicate_records':0,'quality':{'quality_score':100},'reports':['x']}; repo.save_run(run, {'kpis':{'total_revenue':10}}); saved=repo.get_run('r1'); assert saved['status']=='completed'; assert saved['reports']==['x']

def test_runs_list(tmp_path):
    repo=AnalyticsRepository(tmp_path/'x.sqlite3'); assert repo.list_runs()==[]
