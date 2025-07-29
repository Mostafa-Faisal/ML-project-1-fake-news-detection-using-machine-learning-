
"""
BERT Fake News Detection Model Loader
=====================================
Standalone script to load and use the saved BERT fake news detection model.

Usage:
    python model_loader.py "News Title" "News Article Text"
    
Or import in your code:
    from model_loader import load_model, predict_news
    detector = load_model("models/bert_fake_news_detector_YYYYMMDD_HHMMSS.pkl")
    result = predict_news(detector, "Title", "Text")
"""

import pickle
import os
import sys
from typing import Dict, Any
import re
import torch

# Import the standalone detector
from bert_detector import BERTFakeNewsDetector

def load_model(model_path: str):
    """
    Load the BERT fake news detection model from pickle file
    
    Args:
        model_path (str): Path to the pickle file
        
    Returns:
        BERTFakeNewsDetector: Loaded model object
    """
    try:
        # Set device to CPU for loading
        device = torch.device('cpu')
        
        # Load with map_location to handle CUDA/CPU compatibility
        with open(model_path, 'rb') as f:
            if torch.cuda.is_available():
                model = pickle.load(f)
            else:
                # For CPU-only machines, load with CPU mapping
                original_load = torch.load
                torch.load = lambda *args, **kwargs: original_load(*args, **kwargs, map_location='cpu')
                try:
                    model = pickle.load(f)
                finally:
                    torch.load = original_load
        
        print(f"✅ Model loaded successfully from {model_path}")
        return model
    except FileNotFoundError:
        print(f"❌ Model file not found: {model_path}")
        return None
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        # Return a fallback detector instead of None
        print("🔄 Creating fallback detector...")
        return BERTFakeNewsDetector()

def predict_news(model, title: str, text: str) -> Dict[str, Any]:
    """
    Predict if news is fake or real using the loaded model
    
    Args:
        model: Loaded BERTFakeNewsDetector model
        title (str): News article title
        text (str): News article text
        
    Returns:
        Dict: Prediction results
    """
    if model is None:
        return {"error": "Model not loaded"}
    
    try:
        result = model.predict(title, text)
        return result
    except Exception as e:
        return {"error": f"Prediction failed: {e}"}

def find_latest_model(models_dir: str = "models") -> str:
    """
    Find the latest model file in the models directory
    
    Args:
        models_dir (str): Directory containing model files
        
    Returns:
        str: Path to the latest model file
    """
    if not os.path.exists(models_dir):
        return None
    
    model_files = [f for f in os.listdir(models_dir) 
                   if f.startswith("bert_fake_news_detector_") and f.endswith(".pkl")]
    
    if not model_files:
        return None
    
    # Sort by filename (which includes timestamp)
    model_files.sort(reverse=True)
    latest_model = os.path.join(models_dir, model_files[0])
    
    return latest_model

def main():
    """Main function for command line usage"""
    if len(sys.argv) != 3:
        print("Usage: python model_loader.py \"News Title\" \"News Article Text\"")
        sys.exit(1)
    
    title = sys.argv[1]
    text = sys.argv[2]
    
    # Find the latest model
    model_path = find_latest_model()
    if model_path is None:
        print("❌ No model files found in 'models' directory")
        sys.exit(1)
    
    # Load and use the model
    model = load_model(model_path)
    if model is None:
        sys.exit(1)
    
    # Make prediction
    result = predict_news(model, title, text)
    
    if "error" in result:
        print(f"❌ {result['error']}")
        sys.exit(1)
    
    # Display results
    print("=" * 60)
    print(f"🎯 PREDICTION: {result['prediction']}")
    print("=" * 60)
    print(f"📊 Confidence: {result['confidence']:.3f}")
    print(f"🔴 Fake Probability: {result['fake_probability']:.3f}")
    print(f"🟢 Real Probability: {result['real_probability']:.3f}")
    print(f"🔬 Method: {result['method']}")
    print("=" * 60)

if __name__ == "__main__":
    main()
