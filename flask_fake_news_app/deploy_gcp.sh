#!/bin/bash

# GCP App Engine Deployment Script
# Make sure you have Google Cloud SDK installed and authenticated

echo "🚀 Starting GCP App Engine Deployment..."

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK is not installed."
    echo "📥 Please install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "🔐 Please authenticate with Google Cloud:"
    gcloud auth login
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project)
if [ -z "$PROJECT_ID" ]; then
    echo "📝 Please set your project ID:"
    read -p "Enter your GCP Project ID: " PROJECT_ID
    gcloud config set project $PROJECT_ID
fi

echo "📋 Using project: $PROJECT_ID"

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable appengine.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Check if App Engine app exists
if ! gcloud app describe &> /dev/null; then
    echo "🏗️  Creating App Engine application..."
    echo "📍 Available regions:"
    echo "   - us-central1 (Iowa)"
    echo "   - us-east1 (South Carolina)"
    echo "   - europe-west1 (Belgium)"
    echo "   - asia-northeast1 (Tokyo)"
    
    read -p "Enter region (default: us-central1): " REGION
    REGION=${REGION:-us-central1}
    
    gcloud app create --region=$REGION
fi

# Update requirements.txt for App Engine if needed
if ! grep -q "gunicorn" requirements.txt; then
    echo "📦 Adding gunicorn to requirements.txt..."
    echo "gunicorn==21.2.0" >> requirements.txt
fi

# Deploy the application
echo "🚀 Deploying to App Engine..."
gcloud app deploy --quiet

# Get the application URL
APP_URL=$(gcloud app describe --format="value(defaultHostname)")
echo ""
echo "✅ Deployment completed successfully!"
echo "🌐 Your application is available at: https://$APP_URL"
echo ""
echo "📊 Useful commands:"
echo "   View logs: gcloud app logs tail -s default"
echo "   Open app:  gcloud app browse"
echo "   Check status: gcloud app versions list"
echo ""
