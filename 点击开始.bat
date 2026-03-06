@echo off
setlocal
cd /d "%~dp0"

echo ========================================
echo   LLM_AI One-Click Deploy
echo ========================================
echo.

set "PS_EXE=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
if not exist "%PS_EXE%" set "PS_EXE=powershell.exe"

"%PS_EXE%" -NoProfile -ExecutionPolicy Bypass -File "%~dp0deploy.ps1" -Run
if errorlevel 1 (
    echo.
    echo Deploy or startup failed. Check logs above.
    pause
    exit /b 1
)

exit /b 0
