@echo off
REM GCP App Engine Deployment Script for Windows
REM Make sure you have Google Cloud SDK installed and authenticated

echo 🚀 Starting GCP App Engine Deployment...

REM Check if gcloud is installed
where gcloud >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Google Cloud SDK is not installed.
    echo 📥 Please install it from: https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
)

REM Check if user is authenticated
for /f %%i in ('gcloud auth list --filter=status:ACTIVE --format="value(account)"') do set ACCOUNT=%%i
if "%ACCOUNT%"=="" (
    echo 🔐 Please authenticate with Google Cloud:
    gcloud auth login
)

REM Get project ID
for /f %%i in ('gcloud config get-value project') do set PROJECT_ID=%%i
if "%PROJECT_ID%"=="" (
    echo 📝 Please set your project ID:
    set /p PROJECT_ID=Enter your GCP Project ID: 
    gcloud config set project %PROJECT_ID%
)

echo 📋 Using project: %PROJECT_ID%

REM Enable required APIs
echo 🔧 Enabling required APIs...
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com

REM Check if App Engine app exists
gcloud app describe >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo 🏗️  Creating App Engine application...
    echo 📍 Available regions:
    echo    - us-central1 (Iowa)
    echo    - us-east1 (South Carolina)
    echo    - europe-west1 (Belgium)
    echo    - asia-northeast1 (Tokyo)
    
    set /p REGION=Enter region (default: us-central1): 
    if "%REGION%"=="" set REGION=us-central1
    
    gcloud app create --region=%REGION%
)

REM Update requirements.txt for App Engine if needed
findstr /C:"gunicorn" requirements.txt >nul
if %ERRORLEVEL% NEQ 0 (
    echo 📦 Adding gunicorn to requirements.txt...
    echo gunicorn==21.2.0 >> requirements.txt
)

REM Deploy the application
echo 🚀 Deploying to App Engine...
gcloud app deploy --quiet

REM Get the application URL
for /f %%i in ('gcloud app describe --format="value(defaultHostname)"') do set APP_URL=%%i
echo.
echo ✅ Deployment completed successfully!
echo 🌐 Your application is available at: https://%APP_URL%
echo.
echo 📊 Useful commands:
echo    View logs: gcloud app logs tail -s default
echo    Open app:  gcloud app browse
echo    Check status: gcloud app versions list
echo.
pause
