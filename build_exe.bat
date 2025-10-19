@echo off
echo ================================================
echo   WhatsApp Manager - Build EXE
echo ================================================
echo.
echo NOTICE: If build fails due to locked files:
echo   1. Close all WhatsAppManager windows
echo   2. Run REBUILD_EXE.bat instead
echo.
echo Building...
python -m PyInstaller build.spec --clean -y
echo.
if errorlevel 1 (
    echo Build FAILED! See error above.
    echo Try running: REBUILD_EXE.bat
) else (
    echo Build SUCCESS!
    echo EXE location: dist\WhatsAppManager\WhatsAppManager.exe
)
echo.
pause
