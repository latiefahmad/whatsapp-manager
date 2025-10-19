@echo off
echo ================================================
echo   WhatsApp Manager - Rebuild EXE
echo ================================================
echo.
echo Stopping any running instances...
taskkill /F /IM WhatsAppManager.exe 2>nul
timeout /t 2 /nobreak >nul

echo Cleaning old build...
rmdir /S /Q dist 2>nul
rmdir /S /Q build 2>nul
timeout /t 1 /nobreak >nul

echo.
echo Building new EXE...
python -m PyInstaller build.spec --clean -y

if errorlevel 1 (
    echo.
    echo ================================================
    echo   Build FAILED!
    echo ================================================
    echo.
    echo Possible causes:
    echo   1. Python not in PATH
    echo   2. PyInstaller not installed
    echo   3. Files still locked
    echo.
    echo Try:
    echo   1. Close all WhatsAppManager windows
    echo   2. Restart computer
    echo   3. Run this script again
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================
echo   Build SUCCESS!
echo ================================================
echo.
echo EXE location: dist\WhatsAppManager\WhatsAppManager.exe
echo.
echo Press any key to test the app...
pause >nul

start "" "dist\WhatsAppManager\WhatsAppManager.exe"

echo.
echo App launched! Check if it opens without errors.
echo.
pause
