@echo off
setlocal
cd /d "%~dp0"
echo === WPOS PRO V1.0 BUILD ===
python --version || (echo Python tidak ditemukan. & pause & exit /b 1)
if not exist assets\branding\wpos_logo.png (echo Logo WPOS tidak ditemukan. & pause & exit /b 1)
python -m pip install -r requirements.txt pyinstaller || goto fail
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
python -m PyInstaller --clean --noconfirm --windowed --name "WPOS PRO" --paths . --add-data "assets\branding\wpos_logo.png;assets\branding" run.py || goto fail
if not exist "dist\WPOS PRO\WPOS PRO.exe" goto fail
if not exist "dist\WPOS PRO\_internal\assets\branding\wpos_logo.png" goto fail
echo.
echo BUILD BERHASIL: dist\WPOS PRO\WPOS PRO.exe
echo Branding asset: dist\WPOS PRO\_internal\assets\branding\wpos_logo.png
echo.
echo Catatan: data aplikasi disimpan di %%LOCALAPPDATA%%\WPOS PRO saat dijalankan sebagai EXE.
pause
exit /b 0
:fail
echo BUILD GAGAL.
pause
exit /b 1
