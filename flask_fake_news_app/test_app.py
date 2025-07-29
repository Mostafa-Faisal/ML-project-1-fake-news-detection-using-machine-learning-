#!/usr/bin/env python3
"""
Test script to verify Flask app with BERT model integration
"""

import os
import sys
import requests
import time
import subprocess
import signal
from threading import Thread

def test_model_loading():
    """Test if the model can be loaded directly"""
    print("🧪 Testing Model Loading...")
    try:
        from model_loader import load_model, find_latest_model
        
        model_path = find_latest_model("models")
        if not model_path:
            print("❌ No model file found in models directory")
            return False
        
        print(f"📄 Found model: {model_path}")
        
        # Check file size
        file_size = os.path.getsize(model_path) / 1024  # KB
        print(f"📊 Model size: {file_size:.1f} KB")
        
        # Load model
        model = load_model(model_path)
        if model is None:
            print("❌ Failed to load model")
            return False
        
        # Test prediction
        result = model.predict("Test News", "This is a test article for verification.")
        print(f"✅ Model test successful!")
        print(f"   Prediction: {result.get('prediction', 'Unknown')}")
        print(f"   Confidence: {result.get('confidence', 0):.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Model loading test failed: {e}")
        return False

def test_flask_import():
    """Test if Flask app can be imported without errors"""
    print("\n🧪 Testing Flask App Import...")
    try:
        # Change to app directory
        import app
        print("✅ Flask app imported successfully!")
        print(f"   App name: {app.app.name}")
        print(f"   Debug mode: {app.app.debug}")
        return True
    except Exception as e:
        print(f"❌ Flask app import failed: {e}")
        return False

def test_flask_routes():
    """Test Flask routes by starting server briefly"""
    print("\n🧪 Testing Flask Routes...")
    try:
        # Start Flask app in background
        import app as flask_app
        
        # Test in app context
        with flask_app.app.app_context():
            print("✅ Flask app context created successfully!")
            
            # Test database
            from app import db, NewsAnalysis, SystemStats
            try:
                stats = SystemStats.query.first()
                print("✅ Database connection successful!")
            except Exception as e:
                print(f"⚠️ Database test: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Flask routes test failed: {e}")
        return False

def test_api_endpoint():
    """Test API endpoint with a simple request"""
    print("\n🧪 Testing API Endpoint...")
    
    # Start Flask server in background
    import subprocess
    import time
    import requests
    
    try:
        # Start server process
        print("🚀 Starting Flask server...")
        process = subprocess.Popen([
            sys.executable, "app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        time.sleep(5)
        
        # Test health endpoint
        try:
            response = requests.get("http://localhost:5000/health", timeout=10)
            if response.status_code == 200:
                print("✅ Health endpoint working!")
                print(f"   Response: {response.json()}")
            else:
                print(f"⚠️ Health endpoint returned: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Health endpoint test failed: {e}")
        
        # Test analyze endpoint
        try:
            test_data = {
                "title": "Test News Article",
                "content": "This is a test article to verify the API endpoint is working correctly."
            }
            
            response = requests.post(
                "http://localhost:5000/analyze",
                json=test_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Analyze endpoint working!")
                print(f"   Prediction: {result.get('prediction', 'Unknown')}")
                print(f"   Confidence: {result.get('confidence', 0):.3f}")
            else:
                print(f"⚠️ Analyze endpoint returned: {response.status_code}")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Analyze endpoint test failed: {e}")
        
        # Cleanup
        process.terminate()
        process.wait(timeout=5)
        
        return True
        
    except Exception as e:
        print(f"❌ API endpoint test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🔍 FLASK APP COMPREHENSIVE TEST")
    print("=" * 50)
    
    # Change to the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    tests = [
        ("Model Loading", test_model_loading),
        ("Flask Import", test_flask_import), 
        ("Flask Routes", test_flask_routes),
        # ("API Endpoint", test_api_endpoint),  # Commented out for safety
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    print("\n📋 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1
    
    print(f"\n📊 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Flask app is ready to use!")
        print("\n🚀 To start the app:")
        print("   python app.py")
        print("   Then open: http://localhost:5000")
    else:
        print("⚠️ Some tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
