"""
Debug script to see API response
"""
import requests
import json

def debug_api():
    url = "http://localhost:5000/analyze"
    
    test_data = {
        "title": "Test News Title",
        "content": "This is a test news content to check the API response."
    }
    
    try:
        response = requests.post(url, json=test_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"JSON: {json.dumps(result, indent=2)}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_api()
