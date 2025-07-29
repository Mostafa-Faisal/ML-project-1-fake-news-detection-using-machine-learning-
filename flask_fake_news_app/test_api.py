"""
Test script to verify the fake news detection API is working correctly
"""
import requests
import json

def test_fake_news_api():
    url = "http://localhost:5000/analyze"
    
    # Test data
    test_cases = [
        {
            "title": "Scientists Discover New Treatment for Common Cold",
            "content": "Researchers at a major university have published findings in a peer-reviewed journal showing promising results for a new treatment approach.",
            "expected": "Real"
        },
        {
            "title": "DOCTORS SHOCKED: This Ancient Herb Melts Fat Overnight!",
            "content": "URGENT: Big Pharma doesn't want you to know about this MIRACLE herb that has been used for centuries. You won't believe the results!",
            "expected": "Fake"
        }
    ]
    
    print("🧪 Testing Fake News Detection API")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📰 Test Case {i}:")
        print(f"Title: {test_case['title']}")
        print(f"Expected: {test_case['expected']}")
        
        try:
            response = requests.post(url, json={
                'title': test_case['title'],
                'content': test_case['content']
            })
            
            if response.status_code == 200:
                data = response.json()
                if data['success']:
                    result = data['result']
                    print(f"✅ Prediction: {result['prediction']}")
                    print(f"📊 Confidence: {result['confidence']:.3f}")
                    print(f"🔍 Method: {result['method']}")
                    
                    if result['prediction'] == test_case['expected']:
                        print("✅ Test PASSED")
                    else:
                        print("❌ Test FAILED")
                else:
                    print("❌ API returned success=false")
            else:
                print(f"❌ API Error: {response.status_code}")
                print(response.text)
                
        except Exception as e:
            print(f"❌ Request failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 API Test Complete!")

if __name__ == "__main__":
    test_fake_news_api()
