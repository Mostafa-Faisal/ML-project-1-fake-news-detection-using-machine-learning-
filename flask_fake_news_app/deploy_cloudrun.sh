#!/bin/bash

# GCP Cloud Run Deployment Script
# Deploys the application using Docker containers

echo "🐳 Starting GCP Cloud Run Deployment..."

# Configuration
PROJECT_ID=$(gcloud config get-value project)
SERVICE_NAME="fake-news-detector"
REGION="us-central1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

if [ -z "$PROJECT_ID" ]; then
    echo "📝 Please set your project ID:"
    read -p "Enter your GCP Project ID: " PROJECT_ID
    gcloud config set project $PROJECT_ID
fi

echo "📋 Using project: $PROJECT_ID"
echo "🐳 Service name: $SERVICE_NAME"
echo "📍 Region: $REGION"

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com

# Build the container image
echo "🏗️  Building container image..."
gcloud builds submit --tag $IMAGE_NAME

# Deploy to Cloud Run
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $IMAGE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10 \
  --set-env-vars FLASK_ENV=production

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

echo ""
echo "✅ Deployment completed successfully!"
echo "🌐 Your application is available at: $SERVICE_URL"
echo ""
echo "📊 Useful commands:"
echo "   View logs: gcloud run logs tail --service=$SERVICE_NAME --region=$REGION"
echo "   Update service: gcloud run services update $SERVICE_NAME --region=$REGION"
echo "   Delete service: gcloud run services delete $SERVICE_NAME --region=$REGION"
echo ""
