import json

from data_exporter import DataExporter


def test_exports_csv_and_json(tmp_path):
    records = [{"name": "Widget", "price": 12.5, "category": "Tools", "availability": "In Stock"}]
    paths = DataExporter(tmp_path / "output").export(records)
    assert paths.csv_path.exists()
    assert paths.json_path.exists()
    assert "Widget,12.5,Tools,In Stock" in paths.csv_path.read_text(encoding="utf-8")
    assert json.loads(paths.json_path.read_text(encoding="utf-8")) == records
