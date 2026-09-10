from pathlib import Path
import os
import sys

APP_NAME = "WPOS PRO"
APP_VERSION = "V1.0"

# Source/dev: keep project data beside the source tree.
# Frozen Windows build: keep writable data in the user's LocalAppData so
# installation under Program Files does not require administrator rights.
BASE_DIR = Path(__file__).resolve().parent.parent
if getattr(sys, "frozen", False) and os.name == "nt":
    DATA_DIR = Path(os.environ.get("LOCALAPPDATA", Path.home())) / APP_NAME
    BACKUP_DIR = DATA_DIR / "backups"
else:
    DATA_DIR = BASE_DIR / "data"
    BACKUP_DIR = BASE_DIR / "backups"

DATA_DIR.mkdir(parents=True, exist_ok=True)
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DATA_DIR / 'wpos.db'}"
