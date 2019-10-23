from pathlib import Path
import os

PROJECT_DIR = Path(os.environ['UQ_PROJECT'])
RSLT_DIR = PROJECT_DIR / "rslts"
FIG_DIR = PROJECT_DIR / "figures"
INPUT_DIR = PROJECT_DIR / "input"