@echo off

REM Set the name of the virtual environment folder
set VENV_FOLDER=.venv

REM Check if the virtual environment folder exists
if exist "%VENV_FOLDER%" (
    echo Virtual environment folder "%VENV_FOLDER%" already exists.
) else (
    echo Virtual environment folder "%VENV_FOLDER%" not found.
    echo Creating virtual environment...
    
    REM Create the virtual environment
    python -m venv "%VENV_FOLDER%"
    
    if errorlevel 1 (
        echo Failed to create virtual environment. Make sure Python is installed.
        exit /b 1
    )
    
    echo Virtual environment created successfully.
)

REM Activate the virtual environment
call "%VENV_FOLDER%\Scripts\activate"

REM Install required libraries (e.g., from a requirements.txt file)
if exist requirements.txt (
    echo Installing required libraries...
    pip install -r requirements.txt
    
    if errorlevel 1 (
        echo Failed to install required libraries.
        exit /b 1
    )
    
    echo Libraries installed successfully.
) else (
    echo No requirements.txt file found. Skipping library installation.
)

REM Clear the console before starting run.py
cls

REM Launch run.py after the setup
echo Launching run.py...
python run.py

REM Deactivate the virtual environment after the script finishes
deactivate

echo Setup complete.
