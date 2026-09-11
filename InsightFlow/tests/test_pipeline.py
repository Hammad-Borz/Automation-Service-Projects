from pathlib import Path
import pytest
from src.core.pipeline import AnalyticsPipeline

def test_complete_run(settings, frame):
    frame.to_csv(settings.default_input_path,index=False); result=AnalyticsPipeline(settings).run(); assert result['status']=='completed'; assert len(result['reports'])==5; assert result['valid_records']==2

def test_repeated_processing_upserts(settings, frame):
    frame.to_csv(settings.default_input_path,index=False); pipeline=AnalyticsPipeline(settings); pipeline.run(); pipeline.run(); assert len(pipeline.repository.list_records())==2; assert len(pipeline.repository.list_runs())==2

def test_missing_input_fails_and_persists(settings):
    with pytest.raises(FileNotFoundError): AnalyticsPipeline(settings).run(); assert AnalyticsPipeline(settings).repository.list_runs()[0]['status']=='failed'

def test_duplicate_not_double_counted(settings, frame):
    import pandas as pd
    pd.concat([frame,frame.iloc[[0]]],ignore_index=True).to_csv(settings.default_input_path,index=False); result=AnalyticsPipeline(settings).run(); assert result['duplicate_records']==1; assert result['valid_records']==2
