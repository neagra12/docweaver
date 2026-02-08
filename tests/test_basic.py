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
api_key = os.getenv('GEMINI_API_KEY', '')
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

# Test API call with available models
print(f"\n3. Testing API Call:")
# Updated test models list based on your available models
test_models = [
    'gemini-3-flash-preview',      # Gemini 3 (for hackathon)
    'gemini-2.5-flash',            # Latest stable
    'gemini-2.0-flash',            # Alternative
    'gemini-flash-latest'          # Fallback
]

success = False
for model_name in test_models:
    full_model_name = f'models/{model_name}'
    if full_model_name in available_models:
        try:
            print(f"   Testing {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'API is working!'")
            print(f"   ✅ Success with {model_name}")
            print(f"   Response: {response.text}")
            print(f"\n✅ RECOMMENDED MODEL: {model_name}")
            print(f"   Update your config.py to use: GEMINI_MODEL = '{model_name}'")
            success = True
            break
        except Exception as e:
            print(f"   ❌ Failed with {model_name}: {e}")
            continue

if not success:
    print(f"\n   ⚠️  All preferred models failed. Trying any available model...")
    # Try the first available model
    for full_model_name in available_models[:3]:
        model_name = full_model_name.replace('models/', '')
        try:
            print(f"   Testing {model_name}...")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content("Say 'API is working!'")
            print(f"   ✅ Success with {model_name}")
            print(f"   Response: {response.text}")
            print(f"\n✅ WORKING MODEL: {model_name}")
            print(f"   Update your config.py to use: GEMINI_MODEL = '{model_name}'")
            success = True
            break
        except Exception as e:
            print(f"   ❌ Failed with {model_name}: {e}")
            continue

if not success:
    print(f"\n   ❌ All test models failed")
    print(f"   This may be a temporary API issue. Please try again later.")
    exit(1)

print(f"\n" + "="*80)
print(f"SETUP TEST COMPLETE - YOUR CONFIGURATION IS WORKING!")
print(f"="*80)