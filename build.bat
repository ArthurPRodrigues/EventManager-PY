@echo off
REM Simple batch script for local dev (Windows)

setlocal

REM Try 'py' launcher first, fallback to 'python'
where py >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    set PYTHON=py
) else (
    set PYTHON=python
)

set VENV_DIR=.venv
set VENV_PY=%VENV_DIR%\Scripts\python.exe
set VENV_PIP=%VENV_DIR%\Scripts\pip.exe
set VENV_PRECOMMIT=%VENV_DIR%\Scripts\pre-commit.exe

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="install" goto install
if "%1"=="install-dev" goto install_dev
if "%1"=="run" goto run
if "%1"=="clean" goto clean
if "%1"=="play" goto play

echo Unknown target: %1
goto help

:help
echo Targets:
echo   install     - Create venv and install production dependencies
echo   install-dev - Create venv and install all dependencies (prod + dev)
echo   run         - Start the application
echo   clean       - Remove caches and build artifacts
echo   play ^<name^> - Run playground script (e.g., build.bat play friendship)
goto end

:install
if not exist %VENV_DIR% (
    echo Creating virtual environment...
    %PYTHON% -m venv %VENV_DIR%
)
echo Upgrading pip...
%VENV_PIP% install --upgrade pip
echo Installing production dependencies...
%VENV_PIP% install -e .
echo Installation complete!
goto end

:install_dev
if not exist %VENV_DIR% (
    echo Creating virtual environment...
    %PYTHON% -m venv %VENV_DIR%
)
echo Upgrading pip...
%VENV_PIP% install --upgrade pip
echo Installing production dependencies...
%VENV_PIP% install -e .
echo Installing development dependencies...
%VENV_PIP% install -e ".[dev]"
echo Installing pre-commit hooks...
%VENV_PRECOMMIT% install
%VENV_PRECOMMIT% install --hook-type commit-msg
echo Development installation complete!
goto end

:run
echo Starting application...
set PYTHONPATH=src
%VENV_PY% -m main
goto end

:clean
echo Cleaning caches and build artifacts...
if exist __pycache__ rmdir /s /q __pycache__
for /d /r src %%d in (__pycache__) do @if exist "%%d" rmdir /s /q "%%d"
echo Clean complete!
goto end

:play
if "%2"=="" (
    echo Usage: build.bat play ^<script_name^>
    echo Example: build.bat play friendship
    goto end
)
set script_file=src\scripts\play_%2.py
if not exist %script_file% (
    echo Error: Script not found: %script_file%
    goto end
)
echo Running script: %script_file%
set PYTHONPATH=src
%PYTHON% %script_file%
goto end

:end
endlocal
