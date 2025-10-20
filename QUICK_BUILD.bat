@echo off
echo ================================================
echo   WhatsApp Manager - Quick Build
echo ================================================
echo.
echo This will:
echo   1. Build EXE
echo   2. Compile installer (if Inno Setup installed)
echo.
echo Press any key to continue...
pause > nul

echo.
echo Step 1: Building EXE...
echo ================================================
python -m PyInstaller build.spec --clean -y

if errorlevel 1 (
    echo.
    echo Build FAILED! See error above.
    pause
    exit /b 1
)

echo.
echo Build SUCCESS!
echo EXE location: dist\WhatsAppManager\WhatsAppManager.exe
echo.

echo Step 2: Checking for Inno Setup...
echo ================================================
where iscc >nul 2>nul
if %errorlevel% equ 0 (
    echo Inno Setup found! Building installer...
    iscc installer.iss
    if errorlevel 1 (
        echo Installer compilation FAILED!
    ) else (
        echo Installer compiled successfully!
    )
) else (
    echo Inno Setup not found in PATH.
    echo.
    echo To build installer:
    echo   1. Install Inno Setup from https://jrsoftware.org/isdl.php
    echo   2. Add Inno Setup to PATH
    echo   3. Run this script again
    echo.
    echo For now, you can use the EXE from: dist\WhatsAppManager\
)

echo.
echo ================================================
echo   Done!
echo ================================================
pause
