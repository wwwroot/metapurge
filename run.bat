@echo off
echo Starting image-meta-remover application...

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Start the application in background
echo Starting the application...
start /b python app.py

:: Wait for server to initialize (adjust time if needed)
echo Waiting for server to initialize...
timeout /t 3 /nobreak >nul

:: Open browser with the application URL
echo Opening browser...
start http://127.0.0.1:5000

echo Application started successfully.
