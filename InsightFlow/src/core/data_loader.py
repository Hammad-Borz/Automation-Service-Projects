from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {"order_id", "customer_id", "customer_name", "customer_email", "product", "category", "quantity", "unit_price", "total_amount", "order_date", "status", "region", "sales_channel"}


class DataLoadError(ValueError):
    pass


def load_csv(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    try:
        frame = pd.read_csv(path)
    except (OSError, pd.errors.ParserError) as exc:
        raise DataLoadError(f"Unable to read CSV: {exc}") from exc
    columns = {str(column).strip().lower() for column in frame.columns}
    missing = sorted(REQUIRED_COLUMNS - columns)
    if missing:
        raise DataLoadError(f"Missing required columns: {', '.join(missing)}")
    return frame
