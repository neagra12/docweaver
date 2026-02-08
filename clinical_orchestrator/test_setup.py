"""
Test script to verify Gemini API setup
Run this to diagnose configuration issues
"""
import google.generativeai as genai
import os

print("="*80)
print("DOCWEAVER GEMINI API SETUP TEST")
print("="*80)

# Check API key
api_key = os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY')
print(f"\n1. API Key Status:")
if api_key and api_key != 'your_gemini_api_key_here':
    print(f"   ✅ API Key is set")
    print(f"   First 10 chars: {api_key[:10]}...")
else:
    print(f"   ❌ API Key NOT set or using placeholder")
    print(f"   Please set GEMINI_API_KEY environment variable")
    exit(1)

# Configure API
try:
    genai.configure(api_key=api_key)
    print(f"   ✅ API configured successfully")
except Exception as e:
    print(f"   ❌ Failed to configure API: {e}")
    exit(1)

# List available models
print(f"\n2. Available Models:")
try:
    available_models = []
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            available_models.append(model.name)
            print(f"   ✓ {model.name}")
    
    if not available_models:
        print(f"   ❌ No models with generateContent support found")
        exit(1)
except Exception as e:
    print(f"   ❌ Failed to list models: {e}")
    exit(1)

# Test API call with multiple models
print(f"\n3. Testing API Call:")
test_models = [
    'gemini-3-flash-preview',
    'gemini-2.5-flash',
    'gemini-2.0-flash',
    'gemini-flash-latest'
]

success = False
last_error = None

for model_name in test_models:
    full_model_name = f'models/{model_name}'
    if full_model_name in available_models:
        try:
            print(f"\n   Testing {model_name}...")
            model = genai.GenerativeModel(model_name)
            
            # Try a simple generation
            print(f"      → Sending test prompt...")
            response = model.generate_content("Reply with exactly: API is working!")
            
            print(f"   ✅ Success with {model_name}")
            print(f"      Response: {response.text}")
            
            # Check if we have response parts
            if hasattr(response, 'parts'):
                print(f"      Parts: {len(response.parts)}")
            
            # Check prompt feedback
            if hasattr(response, 'prompt_feedback'):
                print(f"      Prompt feedback: {response.prompt_feedback}")
            
            print(f"\n✅ RECOMMENDED MODEL: {model_name}")
            print(f"   Update your config.py to use: GEMINI_MODEL = '{model_name}'")
            success = True
            break
            
        except Exception as e:
            last_error = e
            print(f"   ❌ Failed with {model_name}")
            print(f"      Error type: {type(e).__name__}")
            print(f"      Error message: {str(e)}")
            
            # Print additional error details if available
            if hasattr(e, '__dict__'):
                print(f"      Error details: {e.__dict__}")
            
            continue

if not success:
    print(f"\n❌ ALL MODELS FAILED TO GENERATE CONTENT")
    print(f"\nLast error encountered:")
    print(f"   {last_error}")
    print(f"\nPossible issues:")
    print(f"   1. API key might not have proper permissions")
    print(f"   2. API key might be restricted to certain models")
    print(f"   3. Your account might need to enable Gemini API access")
    print(f"   4. There might be a temporary service issue")
    print(f"\nTroubleshooting steps:")
    print(f"   1. Visit https://aistudio.google.com/")
    print(f"   2. Try generating content in the web UI")
    print(f"   3. Check your API key settings and quotas")
    print(f"   4. Create a new API key if needed")
    exit(1)

print(f"\n" + "="*80)
print(f"SETUP TEST COMPLETE - YOUR CONFIGURATION IS WORKING!")
print(f"="*80)