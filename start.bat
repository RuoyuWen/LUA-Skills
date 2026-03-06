@echo off
setlocal
cd /d "%~dp0"

set "STARTUP_BAT=%~dp0LUA-Skills\lua_story_generator\startup.bat"
if not exist "%STARTUP_BAT%" (
    echo startup.bat not found:
    echo %STARTUP_BAT%
    pause
    exit /b 1
)

call "%STARTUP_BAT%"
exit /b %ERRORLEVEL%
