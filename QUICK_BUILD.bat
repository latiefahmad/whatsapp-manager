@echo off
echo ================================================
echo   WhatsApp Manager - Quick Installer Builder
echo ================================================
echo.
echo This will:
echo   1. Download Inno Setup (if not installed)
echo   2. Compile installer
echo.
echo Press any key to continue...
pause > nul

powershell -ExecutionPolicy Bypass -File setup_and_build_installer.ps1

pause
