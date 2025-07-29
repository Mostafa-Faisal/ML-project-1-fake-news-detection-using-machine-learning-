@echo off
REM Setup script for Fake News Detection Flask App (Windows)

echo 🚀 Setting up Fake News Detection Flask Application...

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo ⚡ Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo 🔄 Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo 📚 Installing Python packages...
pip install -r requirements.txt

REM Download NLTK data
echo 📖 Downloading NLTK data...
python -c "import nltk; import ssl; ssl._create_default_https_context = ssl._create_unverified_context; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4'); nltk.download('punkt_tab'); print('NLTK data downloaded successfully!')"

echo ✅ Setup completed successfully!
echo.
echo 🎯 Next steps:
echo    1. Activate the virtual environment: venv\Scripts\activate
echo    2. Run the application: python app.py
echo    3. Open your browser and go to: http://localhost:5000
echo.
echo 📋 Features available:
echo    • Real-time fake news detection using BERT
echo    • Analysis history with SQLite database
echo    • Statistics and reporting dashboard
echo    • REST API endpoints
echo    • Responsive web interface
echo.
echo 🔧 Troubleshooting:
echo    • If you get import errors, make sure the virtual environment is activated
echo    • If NLTK downloads fail, check your internet connection
echo    • For CUDA/GPU support, install PyTorch with CUDA

pause
