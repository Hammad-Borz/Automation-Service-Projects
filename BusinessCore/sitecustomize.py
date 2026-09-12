import os
import tempfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
TEMP_DIR = PROJECT_ROOT / ".pytest_tmp"
TEMP_DIR.mkdir(exist_ok=True, parents=True)

os.environ.setdefault("TMP", str(TEMP_DIR))
os.environ.setdefault("TEMP", str(TEMP_DIR))
os.environ.setdefault("TMPDIR", str(TEMP_DIR))

tempfile.tempdir = str(TEMP_DIR)
