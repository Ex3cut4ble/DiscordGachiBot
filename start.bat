@echo off

set "DIR=%~dp0"
set "VENV_DIR=%DIR%venv"
set "PYTHON_VENV=%VENV_DIR%\Scripts\python.exe"

if not exist ffmpeg.exe (
    echo FFMPEG not found, installing...
    .\install_ffmpeg.bat
)

if exist "%VENV_DIR%" (
    echo Venv found.
) else (
    echo Venv not found, creating one...
    python -m venv "%VENV_DIR%"
    
    if exist "%PYTHON_VENV%" (
        echo Venv successfully created.
    ) else (
        echo Error occured while creating venv. Exiting...
        exit /b 1
    )

    echo Installing dependencies from requirements.txt...
    "%PYTHON_VENV%" -m pip install -r "%DIR%requirements.txt"

    if %errorlevel% neq 0 (
        echo Error occured while installing dependencies. Exiting...
        exit /b 1
    )
)

echo Starting bot...
"%PYTHON_VENV%" "%DIR%main.py"

echo Bot stopped.
pause