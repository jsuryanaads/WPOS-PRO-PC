from pathlib import Path
from datetime import datetime
import shutil
from ..config import BASE_DIR, BACKUP_DIR

def backup_database():
    source = BASE_DIR / "data" / "wpos.db"
    if not source.exists():
        raise FileNotFoundError("Database belum ada")
    destination = BACKUP_DIR / f"wpos_{datetime.now():%Y%m%d_%H%M%S}.db"
    shutil.copy2(source, destination)
    return destination

def restore_database(path):
    source = Path(path)
    destination = BASE_DIR / "data" / "wpos.db"
    if not source.exists():
        raise FileNotFoundError("Backup tidak ditemukan")
    shutil.copy2(source, destination)
