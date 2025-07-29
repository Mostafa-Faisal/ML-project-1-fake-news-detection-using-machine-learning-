from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from transformers import AutoTokenizer, pipeline
import torch
import logging
import pickle
from model_loader import load_model, find_latest_model
from bert_detector import create_detector

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "fake_news_db.sqlite")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Database Models
class NewsAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    prediction = db.Column(db.String(10), nullable=False)  # 'Real' or 'Fake'
    confidence = db.Column(db.Float, nullable=False)
    fake_probability = db.Column(db.Float, nullable=False)
    real_probability = db.Column(db.Float, nullable=False)
    suspicious_patterns_score = db.Column(db.Float, nullable=False)
    pipeline_score = db.Column(db.Float, nullable=False)
    token_diversity = db.Column(db.Float, nullable=True)
    text_length = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content[:100] + '...' if len(self.content) > 100 else self.content,
            'prediction': self.prediction,
            'confidence': round(self.confidence, 3),
            'fake_probability': round(self.fake_probability, 3),
            'real_probability': round(self.real_probability, 3),
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class SystemStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total_analyses = db.Column(db.Integer, default=0)
    fake_detected = db.Column(db.Integer, default=0)
    real_detected = db.Column(db.Integer, default=0)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

# Initialize the detector using the new BERT implementation
logger.info("🔄 Initializing BERT-based fake news detector...")
try:
    # First, try to load from pickle (with CUDA fix)
    model_path = find_latest_model("models")
    detector = None
    
    if model_path:
        logger.info(f"Found pickle model: {model_path}")
        try:
            detector = load_model(model_path)
            if detector is not None:
                logger.info("✅ Pickle model loaded successfully")
            else:
                logger.warning("⚠️ Pickle model loading failed, using direct implementation")
        except Exception as e:
            logger.warning(f"⚠️ Pickle model loading failed: {e}")
    
    # If pickle loading failed or no model found, use direct implementation
    if detector is None:
        logger.info("🔄 Creating new BERT detector from source...")
        detector = create_detector()
        logger.info("✅ BERT detector initialized successfully from source")
        
except Exception as e:
    logger.error(f"❌ Error initializing detector: {e}")
    logger.info("🔄 Creating fallback detector...")
    detector = create_detector()

# Final safety check
if detector is None:
    logger.error("❌ Critical: Could not initialize any detector!")
    detector = create_detector()

# Routes
@app.route('/')
def index():
    """Home page"""
    # Get recent analyses for display
    recent_analyses = NewsAnalysis.query.order_by(NewsAnalysis.created_at.desc()).limit(5).all()
    
    # Get system statistics
    stats = SystemStats.query.first()
    if not stats:
        stats = SystemStats()
        db.session.add(stats)
        db.session.commit()
    
    return render_template('index.html', recent_analyses=recent_analyses, stats=stats)

@app.route('/analyze', methods=['POST'])
def analyze_news():
    """Analyze news article"""
    try:
        data = request.get_json()
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        
        if not title or not content:
            return jsonify({
                'success': False,
                'message': 'Both title and content are required'
            }), 400
        
        # Perform analysis
        result = detector.predict(title, content)
        
        if result['prediction'] == 'Error':
            return jsonify({
                'success': False,
                'message': f"Analysis error: {result.get('error', 'Unknown error')}"
            }), 500
        
        # Save to database
        analysis = NewsAnalysis(
            title=title,
            content=content,
            prediction=result['prediction'],
            confidence=result['confidence'],
            fake_probability=result['fake_probability'],
            real_probability=result['real_probability'],
            suspicious_patterns_score=result['analysis']['suspicion_patterns'],
            pipeline_score=result['analysis']['pipeline_score'],
            token_diversity=result['analysis']['bert_features']['token_diversity'] if result['analysis']['bert_features'] else None,
            text_length=result['analysis']['bert_features']['text_length'] if result['analysis']['bert_features'] else None,
            ip_address=request.remote_addr
        )
        
        db.session.add(analysis)
        
        # Update statistics
        stats = SystemStats.query.first()
        if not stats:
            stats = SystemStats()
            db.session.add(stats)
        
        stats.total_analyses += 1
        if result['prediction'] == 'Fake':
            stats.fake_detected += 1
        else:
            stats.real_detected += 1
        stats.last_updated = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'result': result,
            'analysis_id': analysis.id
        })
        
    except Exception as e:
        logger.error(f"Error in analyze_news: {e}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/history')
def history():
    """View analysis history"""
    page = request.args.get('page', 1, type=int)
    analyses = NewsAnalysis.query.order_by(NewsAnalysis.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('history.html', analyses=analyses)

@app.route('/api/history')
def api_history():
    """API endpoint for analysis history"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    analyses = NewsAnalysis.query.order_by(NewsAnalysis.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'analyses': [analysis.to_dict() for analysis in analyses.items],
        'total': analyses.total,
        'pages': analyses.pages,
        'current_page': page
    })

@app.route('/stats')
def stats():
    """Statistics page"""
    stats = SystemStats.query.first()
    if not stats:
        stats = SystemStats(total_analyses=0, fake_detected=0, real_detected=0)
    
    # Get recent activity
    recent_analyses = NewsAnalysis.query.order_by(NewsAnalysis.created_at.desc()).limit(10).all()
    
    return render_template('stats.html', stats=stats, recent_analyses=recent_analyses)

@app.route('/api/stats')
def api_stats():
    """API endpoint for statistics"""
    stats = SystemStats.query.first()
    if not stats:
        return jsonify({
            'total_analyses': 0,
            'fake_detected': 0,
            'real_detected': 0,
            'accuracy_note': 'No analyses performed yet'
        })
    
    return jsonify({
        'total_analyses': stats.total_analyses,
        'fake_detected': stats.fake_detected,
        'real_detected': stats.real_detected,
        'fake_percentage': round((stats.fake_detected / stats.total_analyses) * 100, 1) if stats.total_analyses > 0 else 0,
        'real_percentage': round((stats.real_detected / stats.total_analyses) * 100, 1) if stats.total_analyses > 0 else 0,
        'last_updated': stats.last_updated.isoformat() if stats.last_updated else None
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error='Internal server error'), 500

# Create database tables
with app.app_context():
    db.create_all()
    logger.info("✅ Database tables created")

# Health check endpoint for GCP
@app.route('/health')
def health_check():
    """Health check endpoint for load balancers"""
    try:
        # Test database connection
        stats = SystemStats.query.first()
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'database': 'connected'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Get port from environment variable (for GCP deployment)
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    
    print("🚀 Starting Flask Fake News Detection Application...")
    print(f"🔗 Access the application at: http://localhost:{port}")
    print("📊 Features available:")
    print("   • Real-time fake news detection")
    print("   • Analysis history with database storage")
    print("   • Statistics and reporting")
    print("   • REST API endpoints")
    print("   • Responsive web interface")
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
