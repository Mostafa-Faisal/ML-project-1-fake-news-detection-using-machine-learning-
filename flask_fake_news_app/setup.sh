#!/bin/bash

# Setup script for Fake News Detection Flask App

echo "🚀 Setting up Fake News Detection Flask Application..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows (Git Bash)
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi

# Upgrade pip
echo "🔄 Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing Python packages..."
pip install -r requirements.txt

# Download NLTK data
echo "📖 Downloading NLTK data..."
python -c "
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

print('Downloading NLTK data...')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt_tab')
print('NLTK data downloaded successfully!')
"

echo "✅ Setup completed successfully!"
echo ""
echo "🎯 Next steps:"
echo "   1. Activate the virtual environment:"
echo "      - Windows: venv\\Scripts\\activate"
echo "      - Linux/Mac: source venv/bin/activate"
echo "   2. Run the application:"
echo "      python app.py"
echo "   3. Open your browser and go to:"
echo "      http://localhost:5000"
echo ""
echo "📋 Features available:"
echo "   • Real-time fake news detection using BERT"
echo "   • Analysis history with SQLite database"
echo "   • Statistics and reporting dashboard"
echo "   • REST API endpoints"
echo "   • Responsive web interface"
echo ""
echo "🔧 Troubleshooting:"
echo "   • If you get import errors, make sure the virtual environment is activated"
echo "   • If NLTK downloads fail, check your internet connection"
echo "   • For CUDA/GPU support, install PyTorch with CUDA"
