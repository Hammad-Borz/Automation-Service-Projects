from src.core.pipeline import Pipeline


def test_complete_pipeline_and_reports(settings, valid_frame):
    valid_frame.to_csv(settings.default_input_path, index=False)
    result = Pipeline(settings).run()
    assert result["status"] == "completed"
    assert result["valid_records"] == 1
    assert len(result["reports_generated"]) == 5
    assert all(__import__("pathlib").Path(path).exists() for path in result["reports_generated"])


def test_invalid_records_are_handled(settings, valid_frame):
    valid_frame.loc[0, "quantity"] = 0
    valid_frame.to_csv(settings.default_input_path, index=False)
    result = Pipeline(settings).run()
    assert result["status"] == "completed"
    assert result["invalid_records"] == 1
    assert result["valid_records"] == 0


def test_duplicate_handling_is_deterministic(settings, valid_frame):
    import pandas as pd
    frame = pd.concat([valid_frame, valid_frame.assign(order_id="ORD-1")], ignore_index=True)
    frame.to_csv(settings.default_input_path, index=False)
    result = Pipeline(settings).run()
    assert result["duplicate_records"] == 1
    assert result["valid_records"] == 2


def test_pipeline_failure_is_controlled(settings):
    from pytest import raises
    with raises(FileNotFoundError):
        Pipeline(settings).run(settings.default_input_path)
    assert Pipeline(settings).repository.list_runs()[0]["status"] == "failed"
