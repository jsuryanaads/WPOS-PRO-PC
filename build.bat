@echo off
setlocal
cd /d "%~dp0"
echo === WPOS PRO V1.0 BUILD ===
python --version || (echo Python tidak ditemukan. & pause & exit /b 1)
python -m pip install -r requirements.txt pyinstaller || goto fail
python -m PyInstaller --clean --noconfirm --windowed --name "WPOS PRO" app\main.py || goto fail
echo.
echo BUILD BERHASIL: dist\WPOS PRO.exe
pause
exit /b 0
:fail
echo BUILD GAGAL.
pause
exit /b 1
