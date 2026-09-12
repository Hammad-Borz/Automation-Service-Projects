# BusinessCore Setup

Run these commands from the BusinessCore directory:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
pytest
python -m src.main
```

The `.venv` is isolated to BusinessCore. Python 3.12 is the supported interpreter for the pinned dependency set because it provides compatible Windows wheels for all dependencies. Python 3.14 is not used with these pins because Pydantic `2.9.2` and pandas `2.2.3` do not both provide compatible Python 3.14 wheels. Use `python -m pip` after activation so installation and test execution use the same interpreter.