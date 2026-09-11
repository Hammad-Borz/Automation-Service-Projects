from src.core.quality import build_quality_report


def quality_report(processed: dict) -> dict:
    return build_quality_report(len(processed["cleaned"]), processed["validation"], processed["duplicate_count"], len(processed["cleaned"]))
