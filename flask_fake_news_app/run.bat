@echo off
REM Run script for Fake News Detection Flask App (Windows)

echo 🚀 Starting Fake News Detection Flask Application...

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found!
    echo Please run setup.bat first:
    echo    setup.bat
    pause
    exit /b 1
)

REM Activate virtual environment
echo ⚡ Activating virtual environment...
call venv\Scripts\activate.bat

REM Check if Flask is installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ❌ Flask not found! Please run setup.bat first.
    pause
    exit /b 1
)

echo 🔍 Checking system requirements...
python -c "import sys; print(f'Python version: {sys.version}'); import flask; print(f'Flask: ✅ {flask.__version__}'); import transformers; print(f'Transformers: ✅ {transformers.__version__}'); import torch; print(f'PyTorch: ✅ {torch.__version__}'); print(f'CUDA: {'✅ Available' if torch.cuda.is_available() else '⚠️ Not available (using CPU)'}'); import nltk; print(f'NLTK: ✅ {nltk.__version__}')"

echo.
echo 🌐 Starting Flask development server...
echo 📍 Application will be available at: http://localhost:5000
echo 🛑 Press Ctrl+C to stop the server
echo.

REM Run the Flask application
python app.py

pause
