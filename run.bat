@echo off
setlocal

REM Simple batch script for Windows
set PYTHON=python
set VENV_DIR=.venv
set VENV_PYTHON=%VENV_DIR%\Scripts\python.exe
set VENV_PIP=%VENV_DIR%\Scripts\pip.exe

echo EventManager-PY - Windows Runner
echo.

REM Check if virtual environment exists
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    %PYTHON% -m venv %VENV_DIR%
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Install/upgrade dependencies
echo Installing dependencies...
%VENV_PIP% install --upgrade pip
if errorlevel 1 (
    echo Error: Failed to upgrade pip
    pause
    exit /b 1
)

%VENV_PIP% install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install requirements
    pause
    exit /b 1
)

REM Run the application
echo.
echo Starting application...
set PYTHONPATH=src
%VENV_PYTHON% -m main
if errorlevel 1 (
    echo Error: Application failed to start
    pause
    exit /b 1
)

pause
