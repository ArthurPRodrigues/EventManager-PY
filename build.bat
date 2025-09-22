@echo off
REM Windows batch script equivalent to Makefile for local dev
REM Usage: script.bat <command>

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="install-dev" goto install-dev
if "%1"=="run" goto run
goto unknown

:help
echo Targets:
echo   install     - Create venv and install production dependencies
echo   install-dev - Create venv and install all dependencies (prod + dev)
echo   run         - Start the application
echo   help        - Show this help message
goto end

:install
echo Creating virtual environment...
if not exist .venv (
    python -m venv .venv
) else (
    echo Virtual environment already exists.
)

echo Upgrading pip...
.venv\Scripts\pip.exe install --upgrade pip

echo Installing production dependencies...
.venv\Scripts\pip.exe install -e .
echo.
echo Installation completed!
goto end

:install-dev
echo Running install first...
call :install

echo Installing development dependencies...
.venv\Scripts\pip.exe install -e ".[dev]"

if exist .venv\Scripts\pre-commit.exe (
    echo Installing pre-commit hooks...
    .venv\Scripts\pre-commit.exe install
    .venv\Scripts\pre-commit.exe install --hook-type commit-msg
) else (
    echo Warning: pre-commit not found, skipping hook installation.
)

echo.
echo Development installation completed!
goto end

:run
if not exist .venv (
    echo Error: Virtual environment not found. Run 'build.bat install' first.
    goto end
)

echo Starting the application...
set PYTHONPATH=src
.venv\Scripts\python.exe -m main
goto end

:unknown
echo Error: Unknown command '%1'
echo.
echo Use 'build.bat help' to see available commands.
goto end

:end