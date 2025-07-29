# 🛡️ Fake News Detection System with BERT

A comprehensive Flask web application that uses advanced BERT-based Natural Language Processing to detect fake news articles in real-time.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3+-green)
![BERT](https://img.shields.io/badge/BERT-Transformer-orange)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightblue)
![Bootstrap](https://img.shields.io/badge/Frontend-Bootstrap%205-purple)

## ✨ Features

### 🤖 AI-Powered Detection
- **BERT-based Analysis**: Uses state-of-the-art transformer models for contextual understanding
- **Multi-method Approach**: Combines pattern analysis, BERT features, and classification pipelines
- **Real-time Processing**: Instant analysis with confidence scoring
- **Explainable Results**: Detailed breakdown of analysis methods and scores

### 🌐 Web Interface
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Interactive Dashboard**: Real-time statistics and visualizations
- **User-friendly Forms**: Easy-to-use news analysis interface
- **Example Articles**: Pre-loaded examples for testing

### 💾 Database & Analytics
- **SQLite Database**: Stores all analysis history and statistics
- **Analysis History**: Complete record of all processed articles
- **Performance Metrics**: System statistics and detection rates
- **Data Export**: API endpoints for programmatic access

### 🔧 Technical Features
- **REST API**: JSON endpoints for integration with other systems
- **Error Handling**: Comprehensive error management and user feedback
- **Security**: Input validation and sanitization
- **Performance**: Optimized for fast processing and response times

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Internet connection (for downloading models and NLTK data)

### Installation

#### Windows Users
1. **Download and extract the project**
2. **Open Command Prompt or PowerShell in the project directory**
3. **Run the setup script:**
   ```bash
   setup.bat
   ```
4. **Start the application:**
   ```bash
   run.bat
   ```

#### Linux/Mac Users
1. **Clone or download the project**
2. **Open terminal in the project directory**
3. **Make scripts executable:**
   ```bash
   chmod +x setup.sh run.sh
   ```
4. **Run the setup script:**
   ```bash
   ./setup.sh
   ```
5. **Start the application:**
   ```bash
   ./run.sh
   ```

#### Manual Installation
If the scripts don't work, you can set up manually:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet'); nltk.download('omw-1.4'); nltk.download('punkt_tab')"

# Run the application
python app.py
```

### 🌐 Access the Application
Once running, open your web browser and navigate to:
```
http://localhost:5000
```

## 📱 Usage Guide

### 1. Analyzing News Articles
1. Navigate to the home page
2. Enter the news article title and content
3. Click "Analyze News Article"
4. Review the detailed results including:
   - Prediction (Real/Fake)
   - Confidence score
   - Detailed analysis breakdown

### 2. Using Example Articles
- Click "Real News Example" or "Fake News Example" buttons
- Pre-loaded examples will fill the form
- Great for testing and understanding the system

### 3. Viewing History
- Navigate to "History" in the top menu
- See all previously analyzed articles
- Click "View" for detailed analysis information
- Pagination for large datasets

### 4. Checking Statistics
- Navigate to "Statistics" in the top menu
- View system performance metrics
- See detection distribution charts
- Monitor recent activity

## 🏗️ System Architecture

### Backend Components
```
├── app.py                 # Main Flask application
├── models/
│   ├── BERTFakeNewsDetector  # Core AI detection class
│   └── Database Models       # SQLAlchemy models
├── templates/             # HTML templates
├── static/               # CSS, JS, and assets
└── requirements.txt      # Python dependencies
```

### AI Detection Pipeline
1. **Text Preprocessing**: Cleaning and tokenization
2. **BERT Tokenization**: Advanced tokenization using transformers
3. **Pattern Analysis**: Detection of suspicious keywords and patterns
4. **Classification Pipeline**: ML model predictions
5. **Score Combination**: Weighted average of all methods
6. **Confidence Calculation**: Statistical confidence in prediction

### Database Schema
- **NewsAnalysis**: Stores analysis results and metadata
- **SystemStats**: Tracks overall system statistics
- **Automatic Indexing**: Optimized for quick queries

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production deployment:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///fake_news_db.sqlite
FLASK_ENV=production
```

### Model Configuration
The system uses these models by default:
- **Base Model**: `distilbert-base-uncased`
- **Classification Pipeline**: `martin-ha/toxic-comment-model`

To use different models, modify the `BERTFakeNewsDetector` class in `app.py`.

## 📊 API Documentation

### Analyze News Endpoint
```http
POST /analyze
Content-Type: application/json

{
    "title": "News article title",
    "content": "Full article content"
}
```

**Response:**
```json
{
    "success": true,
    "result": {
        "prediction": "Real",
        "confidence": 0.85,
        "fake_probability": 0.15,
        "real_probability": 0.85,
        "analysis": {
            "suspicion_patterns": 0.1,
            "pipeline_score": 0.2,
            "bert_features": {
                "token_diversity": 0.7,
                "text_length": 256
            }
        }
    },
    "analysis_id": 123
}
```

### Statistics Endpoint
```http
GET /api/stats
```

### History Endpoint
```http
GET /api/history?page=1&per_page=10
```

## 🧪 Testing Examples

### Real News Example
```
Title: "Climate Change Research Shows Alarming Trends"
Content: "A comprehensive study published in Nature Climate Change reveals..."
Expected: Real (High confidence)
```

### Fake News Example
```
Title: "SHOCKING: Miracle Cure Big Pharma Doesn't Want You to Know!"
Content: "URGENT UPDATE: Secret government study reveals AMAZING natural cure..."
Expected: Fake (High confidence)
```

## 🛠️ Development

### Project Structure
```
flask_fake_news_app/
├── app.py                    # Main application
├── requirements.txt          # Dependencies
├── setup.sh / setup.bat     # Setup scripts
├── run.sh / run.bat         # Run scripts
├── templates/               # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── history.html
│   ├── stats.html
│   └── error.html
├── static/
│   ├── css/
│   │   └── style.css        # Custom styles
│   └── js/
│       └── main.js          # JavaScript functions
└── README.md               # This file
```

### Adding New Features
1. **Backend**: Extend Flask routes in `app.py`
2. **Frontend**: Add templates and update JavaScript
3. **Database**: Create new models using SQLAlchemy
4. **AI Models**: Extend the `BERTFakeNewsDetector` class

### Database Migration
For production deployments with data migration needs:
```python
from flask_migrate import Migrate
# Add migration support
```

## 🚀 Deployment

### Local Development
Use the provided scripts for local development and testing.

### Production Deployment
1. **Set Environment Variables**
2. **Use Production WSGI Server** (Gunicorn, uWSGI)
3. **Configure Reverse Proxy** (Nginx, Apache)
4. **Set up SSL/HTTPS**
5. **Configure Database** (PostgreSQL for production)

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt`

2. **NLTK Download Errors**
   - Check internet connection
   - Run NLTK downloads manually

3. **CUDA/GPU Issues**
   - Install PyTorch with CUDA support if needed
   - System will fall back to CPU automatically

4. **Port Already in Use**
   - Change port in `app.py`: `app.run(port=5001)`
   - Or kill the process using port 5000

5. **Database Errors**
   - Delete `fake_news_db.sqlite` to reset database
   - Restart the application

### Performance Optimization
- **GPU Acceleration**: Install CUDA-compatible PyTorch
- **Model Caching**: Models are cached after first load
- **Database Indexing**: Automatic indexing on frequently queried fields

## 📈 Future Enhancements

### Planned Features
- [ ] **User Authentication**: User accounts and personal history
- [ ] **Batch Processing**: Upload and analyze multiple articles
- [ ] **API Rate Limiting**: Prevent abuse of API endpoints
- [ ] **Advanced Analytics**: More detailed statistical analysis
- [ ] **Model Fine-tuning**: Domain-specific model training
- [ ] **Multi-language Support**: Support for non-English articles
- [ ] **Real-time Monitoring**: Live news feed analysis
- [ ] **Export Features**: PDF reports and CSV downloads

### Research Extensions
- [ ] **Cross-lingual Detection**: Support multiple languages
- [ ] **Bias Analysis**: Detect political or ideological bias
- [ ] **Source Credibility**: Rate news sources
- [ ] **Fact-checking Integration**: Link to fact-checking services
- [ ] **Social Media Integration**: Analyze social media posts

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Hugging Face Transformers**: For BERT model implementation
- **Flask Community**: For the excellent web framework
- **Bootstrap**: For the responsive UI components
- **NLTK Team**: For natural language processing tools
- **PyTorch Team**: For the deep learning framework

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation

## 🔗 Links

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Transformers Library](https://huggingface.co/transformers/)
- [BERT Paper](https://arxiv.org/abs/1810.04805)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)

---

**Built with ❤️ using BERT, Flask, and modern web technologies**
