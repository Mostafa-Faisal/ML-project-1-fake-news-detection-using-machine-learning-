#!/bin/bash

# Run script for Fake News Detection Flask App

echo "🚀 Starting Fake News Detection Flask Application..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup.sh first:"
    echo "   bash setup.sh"
    exit 1
fi

# Activate virtual environment
echo "⚡ Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows (Git Bash)
    source venv/Scripts/activate
else
    # Linux/Mac
    source venv/bin/activate
fi

# Check if Flask is installed
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Flask not found! Please run setup.sh first."
    exit 1
fi

echo "🔍 Checking system requirements..."
python -c "
import sys
print(f'Python version: {sys.version}')

try:
    import flask
    print(f'Flask: ✅ {flask.__version__}')
except ImportError:
    print('Flask: ❌ Not installed')

try:
    import transformers
    print(f'Transformers: ✅ {transformers.__version__}')
except ImportError:
    print('Transformers: ❌ Not installed')

try:
    import torch
    print(f'PyTorch: ✅ {torch.__version__}')
    if torch.cuda.is_available():
        print(f'CUDA: ✅ Available ({torch.cuda.device_count()} devices)')
    else:
        print('CUDA: ⚠️ Not available (using CPU)')
except ImportError:
    print('PyTorch: ❌ Not installed')

try:
    import nltk
    print(f'NLTK: ✅ {nltk.__version__}')
except ImportError:
    print('NLTK: ❌ Not installed')
"

echo ""
echo "🌐 Starting Flask development server..."
echo "📍 Application will be available at: http://localhost:5000"
echo "🛑 Press Ctrl+C to stop the server"
echo ""

# Run the Flask application
python app.py
