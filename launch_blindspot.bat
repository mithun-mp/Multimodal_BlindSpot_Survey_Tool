@echo off
setlocal
cd /d "%~dp0"
title BlindSpot Workstation
set "PYTHONPATH=%~dp0;%PYTHONPATH%"

python -m blindspot.launcher %*
if errorlevel 1 (
    echo.
    echo [ERROR] BlindSpot failed to start or exited with error code %errorlevel%.
    echo Please verify Python is installed and accessible in your PATH.
    echo.
    pause
)
