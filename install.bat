@echo off
echo Setting up Student Portal Django Project...
echo ===========================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Python found.

REM Check if virtual environment exists, create if not
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo Virtual environment already exists.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install requirements
if exist requirements.txt (
    echo Installing requirements...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ERROR: Failed to install requirements.
        pause
        exit /b 1
    )
) else (
    echo WARNING: requirements.txt not found.
)

REM Navigate to project directory
cd "project file\Youtube\django\studentstudyportal"

REM Run migrations
echo Running database migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Failed to run migrations.
    pause
    exit /b 1
)

REM Collect static files
echo Collecting static files...
python manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo ERROR: Failed to collect static files.
    pause
    exit /b 1
)

REM Copy images if script exists
if exist "..\..\..\..\..\copy_images.py" (
    echo Copying images...
    python "..\..\..\..\..\copy_images.py"
)

echo ===========================================
echo Setup completed successfully!
echo To run the server, activate the virtual environment and run:
echo cd "project file\Youtube\django\studentstudyportal"
echo call venv\Scripts\activate
echo python manage.py runserver
echo ===========================================
pause