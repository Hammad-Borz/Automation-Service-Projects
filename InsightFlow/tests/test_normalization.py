from src.core.normalizer import normalize_frame

def test_whitespace_case_email_and_total(frame):
    row=normalize_frame(frame).iloc[0]; assert row.customer_name=='Alice'; assert row.customer_email=='alice@example.com'; assert row.status=='completed'; assert row.region=='North America'; assert row.sales_channel=='online'; assert row.calculated_total==1200

def test_date_is_datetime(frame): assert str(normalize_frame(frame).order_date.dtype).startswith('datetime')

def test_numeric_conversion(frame): assert normalize_frame(frame).quantity.dtype.kind in 'iu'; assert normalize_frame(frame).unit_price.dtype.kind in 'fi'

def test_empty_value_becomes_none(frame):
    import pandas as pd
    frame.loc[0,'customer_name']=' '; assert pd.isna(normalize_frame(frame).iloc[0].customer_name)
