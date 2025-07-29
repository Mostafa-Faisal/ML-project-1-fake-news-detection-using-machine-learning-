from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import re

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'demo-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fake_news_demo.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# Database Models
class NewsAnalysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    prediction = db.Column(db.String(10), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    fake_probability = db.Column(db.Float, nullable=False)
    real_probability = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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

# Simple Fake News Detector (Demo Version)
class SimpleFakeNewsDetector:
    def __init__(self):
        self.suspicious_patterns = [
            'shocking', 'exclusive', 'secret', 'urgent', 'miracle', 'breaking',
            'doctors hate', 'one weird trick', 'you won\'t believe', 'leaked',
            'government cover', 'big pharma', 'they don\'t want you to know',
            'amazing discovery', 'scientists shocked', 'unbelievable', 'incredible'
        ]
    
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
            pattern_count * 0.4 +
            caps_ratio * 0.5 +
            min(exclamation_count / 5, 0.3)
        )
        
        return min(suspicion_score, 1.0)
    
    def predict(self, title, text):
        """Simple prediction based on pattern analysis"""
        combined_text = f"{title} {text}"
        
        # Pattern-based analysis
        suspicion_score = self.analyze_suspicious_patterns(combined_text)
        
        # Simple heuristics
        text_length = len(text)
        title_length = len(title)
        
        # Shorter texts are often more suspicious
        length_factor = 0.3 if text_length < 100 else 0.1
        
        # Very long titles are suspicious
        title_factor = 0.2 if title_length > 100 else 0.0
        
        # Final score calculation
        final_score = min(suspicion_score + length_factor + title_factor, 1.0)
        
        # Determine prediction
        is_fake = final_score > 0.5
        confidence = abs(final_score - 0.5) * 2
        
        return {
            'prediction': 'Fake' if is_fake else 'Real',
            'confidence': confidence,
            'fake_probability': final_score,
            'real_probability': 1 - final_score,
            'analysis': {
                'suspicion_patterns': suspicion_score,
                'length_factor': length_factor,
                'title_factor': title_factor
            },
            'method': 'Pattern-based Analysis (Demo)'
        }

# Initialize the detector
detector = SimpleFakeNewsDetector()

# Routes
@app.route('/')
def index():
    """Home page"""
    recent_analyses = NewsAnalysis.query.order_by(NewsAnalysis.created_at.desc()).limit(5).all()
    
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
        
        # Save to database
        analysis = NewsAnalysis(
            title=title,
            content=content,
            prediction=result['prediction'],
            confidence=result['confidence'],
            fake_probability=result['fake_probability'],
            real_probability=result['real_probability']
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

@app.route('/stats')
def stats():
    """Statistics page"""
    stats = SystemStats.query.first()
    if not stats:
        stats = SystemStats(total_analyses=0, fake_detected=0, real_detected=0)
    
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

if __name__ == '__main__':
    print("🚀 Starting Flask Fake News Detection Demo Application...")
    print("🔗 Access the application at: http://localhost:5001")
    print("📊 Features available:")
    print("   • Simple pattern-based fake news detection")
    print("   • Analysis history with database storage")
    print("   • Statistics and reporting")
    print("   • Responsive web interface")
    print("   • No heavy model downloads required!")
    app.run(debug=True, host='0.0.0.0', port=5001)
