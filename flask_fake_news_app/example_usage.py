
"""
Example usage of the BERT Fake News Detection Model
"""

from model_loader import load_model, predict_news, find_latest_model

# Load the latest model
model_path = find_latest_model()
print(f"Loading model from: {model_path}")

detector = load_model(model_path)

# Test examples
test_cases = [
    {
        "title": "Scientists Discover New Cancer Treatment",
        "text": "Researchers at Johns Hopkins University have developed a promising new immunotherapy approach for treating various forms of cancer.",
        "expected": "Real"
    },
    {
        "title": "SHOCKING: This One Weird Trick Doctors Don't Want You to Know!",
        "text": "URGENT: Big Pharma is hiding this AMAZING secret that can cure all diseases instantly! Click here to learn more!",
        "expected": "Fake"
    }
]

print("\n" + "="*50)
print("TESTING LOADED MODEL")
print("="*50)

for i, test in enumerate(test_cases, 1):
    print(f"\nTest {i}: {test['expected']} News")
    print(f"Title: {test['title']}")
    print(f"Text: {test['text'][:50]}...")
    
    result = predict_news(detector, test['title'], test['text'])
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        continue
    
    print(f"🎯 Prediction: {result['prediction']}")
    print(f"📊 Confidence: {result['confidence']:.3f}")
    print(f"✅ Correct: {'Yes' if result['prediction'] == test['expected'] else 'No'}")

print("\n✅ Model testing complete!")
