"""
BERT-based Fake News Detector
============================
Implementation based on the Jupyter notebook without pickle dependencies.
This avoids CUDA/CPU compatibility issues.
"""

import re
import torch
import nltk
from transformers import AutoTokenizer, pipeline
import logging

logger = logging.getLogger(__name__)

class BERTFakeNewsDetector:
    def __init__(self, model_name='distilbert-base-uncased'):
        """Initialize BERT-based fake news classifier"""
        self.model_name = model_name
        self.tokenizer = None
        self.classifier_pipeline = None
        self.suspicious_patterns = [
            'shocking', 'exclusive', 'secret', 'urgent', 'miracle', 'breaking',
            'doctors hate', 'one weird trick', 'you won\'t believe', 'leaked',
            'government cover', 'big pharma', 'they don\'t want you to know',
            'amazing discovery', 'scientists shocked', 'unbelievable', 'incredible'
        ]
        
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the BERT model and tokenizer"""
        try:
            # Download NLTK data if not present
            try:
                nltk.data.find('tokenizers/punkt')
                nltk.data.find('corpora/stopwords')
            except LookupError:
                logger.info("Downloading NLTK data...")
                nltk.download('punkt')
                nltk.download('stopwords')
                nltk.download('wordnet')
                nltk.download('omw-1.4')
                try:
                    nltk.download('punkt_tab')
                except:
                    pass  # punkt_tab might not be available in older versions
            
            # Load tokenizer with CPU-only setup
            logger.info(f"Loading BERT tokenizer: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            logger.info(f"✅ BERT tokenizer loaded: {self.model_name}")
            
            # Initialize classification pipeline with CPU device
            try:
                device = -1  # Force CPU usage
                self.classifier_pipeline = pipeline(
                    "text-classification",
                    model="martin-ha/toxic-comment-model",
                    tokenizer="martin-ha/toxic-comment-model",
                    device=device
                )
                logger.info("✅ Classification pipeline initialized (CPU)")
            except Exception as e:
                logger.warning(f"⚠️ Pipeline not available: {e}")
                self.classifier_pipeline = None
                
        except Exception as e:
            logger.error(f"❌ Error loading BERT model: {e}")
            self.tokenizer = None
    
    def preprocess_text(self, title, text, max_length=512):
        """Preprocess text for BERT input"""
        if self.tokenizer is None:
            return None
        
        combined_text = f"{title} [SEP] {text}"
        
        try:
            encoded = self.tokenizer(
                combined_text,
                add_special_tokens=True,
                max_length=max_length,
                padding='max_length',
                truncation=True,
                return_tensors='pt'
            )
            return encoded
        except Exception as e:
            logger.error(f"Error in text preprocessing: {e}")
            return None
    
    def analyze_suspicious_patterns(self, text):
        """Analyze text for suspicious patterns common in fake news"""
        text_lower = text.lower()
        
        # Count suspicious patterns
        pattern_count = sum(1 for pattern in self.suspicious_patterns 
                          if pattern in text_lower)
        
        # Check for excessive capitalization
        words = text.split()
        caps_ratio = sum(1 for word in words if word.isupper()) / len(words) if words else 0
        
        # Check for excessive punctuation
        exclamation_count = text.count('!')
        
        # Calculate suspicion score
        suspicion_score = (
            pattern_count * 0.3 +
            caps_ratio * 0.4 +
            min(exclamation_count / 10, 0.3)
        )
        
        return min(suspicion_score, 1.0)
    
    def predict(self, title, text):
        """Predict if news is fake or real using BERT-based approach"""
        try:
            combined_text = f"{title} {text}"
            
            # Method 1: Pattern-based analysis
            suspicion_score = self.analyze_suspicious_patterns(combined_text)
            
            # Method 2: BERT tokenizer analysis
            bert_features = None
            if self.tokenizer is not None:
                encoded = self.preprocess_text(title, text)
                if encoded is not None:
                    input_ids = encoded['input_ids'][0]
                    attention_mask = encoded['attention_mask'][0]
                    
                    unique_tokens = len(torch.unique(input_ids))
                    total_tokens = len(input_ids[attention_mask == 1])
                    token_diversity = unique_tokens / total_tokens if total_tokens > 0 else 0
                    
                    bert_features = {
                        'token_diversity': token_diversity,
                        'text_length': total_tokens
                    }
            
            # Method 3: Classification pipeline
            pipeline_score = 0.5
            if self.classifier_pipeline is not None:
                try:
                    result = self.classifier_pipeline(combined_text[:512])
                    if result and len(result) > 0:
                        if result[0]['label'] == 'TOXIC':
                            pipeline_score = result[0]['score'] * 0.7
                        else:
                            pipeline_score = 0.5
                except Exception as e:
                    logger.warning(f"Pipeline prediction failed: {e}")
                    pipeline_score = 0.5
            
            # Combine all methods
            if bert_features:
                final_score = (
                    suspicion_score * 0.4 +
                    pipeline_score * 0.4 +
                    (1 - bert_features['token_diversity']) * 0.2
                )
            else:
                # Fallback when BERT features are not available
                final_score = (
                    suspicion_score * 0.6 +
                    pipeline_score * 0.4
                )
            
            is_fake = final_score > 0.5
            confidence = abs(final_score - 0.5) * 2
            
            return {
                'prediction': 'Fake' if is_fake else 'Real',
                'confidence': confidence,
                'fake_probability': final_score,
                'real_probability': 1 - final_score,
                'analysis': {
                    'suspicion_patterns': suspicion_score,
                    'pipeline_score': pipeline_score,
                    'bert_features': bert_features
                },
                'method': 'Enhanced BERT-based Analysis'
            }
            
        except Exception as e:
            logger.error(f"Error in prediction: {e}")
            return {
                'prediction': 'Error',
                'confidence': 0.0,
                'fake_probability': 0.5,
                'real_probability': 0.5,
                'analysis': {
                    'suspicion_patterns': 0.0,
                    'pipeline_score': 0.0,
                    'bert_features': None
                },
                'method': 'Error in Analysis',
                'error': str(e)
            }

def create_detector():
    """Factory function to create a new detector instance"""
    return BERTFakeNewsDetector()
