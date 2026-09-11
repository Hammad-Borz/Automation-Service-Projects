import pandas as pd
import pytest
from src.core.data_loader import load_csv, DataLoadError

def test_valid_csv(frame, tmp_path):
    path=tmp_path/'x.csv'; frame.to_csv(path,index=False); assert len(load_csv(path))==2

def test_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError): load_csv(tmp_path/'x.csv')

def test_missing_columns(tmp_path):
    path=tmp_path/'x.csv'; pd.DataFrame({'order_id':['1']}).to_csv(path,index=False)
    with pytest.raises(DataLoadError, match='Missing required'): load_csv(path)

def test_malformed_csv(tmp_path):
    path=tmp_path/'x.csv'; path.write_text('order_id,customer_id\n"bad', encoding='utf-8')
    with pytest.raises(DataLoadError): load_csv(path)
