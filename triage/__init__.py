from pathlib import Path

TRIAGE_DIR = Path(__file__).parent
PROJECT_DIR = TRIAGE_DIR.parent
DATA_DIR = PROJECT_DIR / "data"
LOGS_DIR = DATA_DIR / "logs"
CHANGES_DIR = DATA_DIR / "changes"
INCIDENTS_DIR = DATA_DIR / "incidents"
RUNBOOK_DIR = DATA_DIR / "runbook"
OUTDIR = PROJECT_DIR / "out"
LOG_FILE_NAME = "comms.log"
LOG_FILE_PATH = OUTDIR / LOG_FILE_NAME
