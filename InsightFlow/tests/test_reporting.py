from pathlib import Path
import json
from src.core.report_engine import generate_reports
from src.core.analytics_engine import analyze
from src.core.normalizer import normalize_frame
from src.services.insight_service import generate_insights

def test_all_report_formats(tmp_path, frame):
    normalized=normalize_frame(frame); analytics=analyze(normalized); paths=generate_reports(normalized, analytics, generate_insights(analytics), {'quality_score':100}, tmp_path); assert len(paths)==5; assert all(Path(path).exists() for path in paths)

def test_json_report_is_structured(tmp_path, frame):
    normalized=normalize_frame(frame); analytics=analyze(normalized); generate_reports(normalized, analytics, [], {'quality_score':100}, tmp_path); data=json.loads((tmp_path/'analytics_report.json').read_text()); assert 'analytics' in data; assert 'quality' in data

def test_summary_contains_kpis(tmp_path, frame):
    normalized=normalize_frame(frame); analytics=analyze(normalized); generate_reports(normalized, analytics, [], {'quality_score':100}, tmp_path); text=(tmp_path/'executive_summary.txt').read_text(); assert 'Total revenue' in text; assert 'Average order value' in text
