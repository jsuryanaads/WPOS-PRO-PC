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

## Menjalankan
```bash
python -m app.main
```

## Build EXE Windows
Jalankan `build.bat` atau `CLEAN_BUILD.bat` di Windows setelah Python dan dependensi tersedia.

## Installer
Compile `installer.iss` menggunakan Inno Setup setelah `dist\WPOS PRO.exe` berhasil dibuat.

## Repository workflow
GitHub adalah source of truth proyek. ZIP hanya dibuat untuk milestone/final release, bukan setiap perubahan.
