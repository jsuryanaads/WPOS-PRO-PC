# WPOS PRO V1.0

POS toko sembako Windows offline, satu komputer.

## Teknologi
- Python 3.11+
- PySide6
- SQLite
- SQLAlchemy
- PyInstaller
- Inno Setup

## Default login
- Username: `admin`
- Password: `admin123`

**Penting:** ubah password default sebelum produksi.

## Menjalankan dari source
```bat
python -m app.main
```

## Testing
```bat
pytest -q
```

## Build EXE
Jalankan `build.bat` pada Windows dengan Python dan PyInstaller terpasang.

## Installer
Compile `installer.iss` menggunakan Inno Setup setelah EXE berhasil dibuat.

## Status
Repository ini adalah master source pengembangan WPOS PRO V1.0. ZIP hanya dibuat pada milestone/final release.
