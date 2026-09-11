import pandas as pd
from src.core.validator import validate_frame

def base(**changes):
    row={'order_id':'1','customer_id':'c','customer_name':'A','customer_email':'a@example.com','product':'P','category':'C','quantity':1,'unit_price':2,'total_amount':2,'order_date':'2026-01-01','status':'completed','region':'East','sales_channel':'online'}; row.update(changes); return pd.DataFrame([row])

def test_valid(): assert validate_frame(base())[0].valid

def test_missing_order_id(): assert 'order_id is required' in validate_frame(base(order_id=''))[0].errors

def test_missing_customer_id(): assert 'customer_id is required' in validate_frame(base(customer_id=None))[0].errors

def test_invalid_quantity(): assert not validate_frame(base(quantity=0))[0].valid

def test_invalid_price_and_total():
    errors=validate_frame(base(unit_price=-1,total_amount='bad'))[0].errors; assert 'unit_price must be a non-negative number' in errors; assert 'total_amount must be a non-negative number' in errors

def test_invalid_date_status_channel():
    errors=validate_frame(base(order_date='bad',status='shipped',sales_channel='phone'))[0].errors; assert 'order_date is invalid' in errors; assert 'status is unsupported' in errors; assert 'sales_channel is unsupported' in errors

def test_invalid_email_and_region():
    errors=validate_frame(base(customer_email='bad',region=''))[0].errors; assert 'customer_email is invalid' in errors; assert 'region is required' in errors
