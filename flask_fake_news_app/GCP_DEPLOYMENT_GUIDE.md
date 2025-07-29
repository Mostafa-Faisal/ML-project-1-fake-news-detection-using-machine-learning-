# 🚀 Quick GCP Deployment Guide

## Prerequisites
1. **Google Cloud Account**: Create at https://cloud.google.com
2. **Google Cloud SDK**: Install from https://cloud.google.com/sdk/docs/install
3. **Project Setup**: Create a new GCP project

## 🎯 Choose Your Deployment Method

### Option 1: App Engine (Easiest - Recommended)
```bash
# Windows
deploy_gcp.bat

# Linux/Mac
chmod +x deploy_gcp.sh
./deploy_gcp.sh
```

### Option 2: Cloud Run (Docker-based)
```bash
# Linux/Mac
chmod +x deploy_cloudrun.sh
./deploy_cloudrun.sh
```

### Option 3: Manual App Engine Deployment
```bash
# 1. Install Google Cloud SDK
# 2. Authenticate
gcloud auth login

# 3. Set project
gcloud config set project YOUR_PROJECT_ID

# 4. Enable APIs
gcloud services enable appengine.googleapis.com

# 5. Create App Engine app
gcloud app create --region=us-central1

# 6. Deploy
gcloud app deploy

# 7. Open in browser
gcloud app browse
```

## 📋 Project Structure for GCP
```
flask_fake_news_app/
├── app.py                 # Main application
├── app.yaml              # App Engine configuration
├── Dockerfile            # For Cloud Run
├── requirements.txt      # Python dependencies
├── deploy_gcp.sh/.bat   # Deployment scripts
├── .gcloudignore        # Files to ignore
└── templates/           # HTML templates
```

## 💰 Estimated Costs

### App Engine
- **Free Tier**: 28 instance hours/day
- **Light Usage**: $5-20/month
- **Medium Usage**: $20-100/month

### Cloud Run
- **Free Tier**: 2M requests/month
- **Pay-per-use**: Very cost-effective for low traffic

## 🔧 Post-Deployment

1. **Test the application**: Visit the provided URL
2. **Monitor logs**: `gcloud app logs tail -s default`
3. **Update app**: Re-run deployment script
4. **Scale if needed**: Adjust `app.yaml` settings

## 🆘 Troubleshooting

### Common Issues:
1. **Quota Exceeded**: Enable billing on your project
2. **Region Error**: Choose a supported App Engine region
3. **Build Timeout**: Increase timeout in `app.yaml`
4. **Memory Issues**: Increase memory allocation

### Support Commands:
```bash
# View logs
gcloud app logs tail -s default

# Check app status
gcloud app versions list

# SSH to instance (Compute Engine only)
gcloud compute ssh INSTANCE_NAME

# Delete version
gcloud app versions delete VERSION_ID
```

## 🌐 Access Your App

After successful deployment:
- **App Engine**: `https://YOUR_PROJECT_ID.appspot.com`
- **Cloud Run**: `https://SERVICE_NAME-HASH-uc.a.run.app`

## 🔒 Security Notes

1. Change the SECRET_KEY in `app.yaml`
2. Use Cloud SQL for production database
3. Enable HTTPS (automatic on GCP)
4. Set up monitoring and alerting

**Your Flask Fake News Detection app is ready for the cloud!** 🎉
