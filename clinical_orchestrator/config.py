"""
Configuration management for DocWeaver
Tracks API calls and manages Gemini settings
"""
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()


class Config:
    """Central configuration for DocWeaver"""
    
    # API Configuration
    # Note: Using GEMINI_API_KEY as the standard name (not GOOGLE_API_KEY)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    
    if not GEMINI_API_KEY:
        print("="*80)
        print("⚠️  WARNING: GEMINI_API_KEY NOT CONFIGURED!")
        print("="*80)
        print("\nPlease set your API key using ONE of these methods:\n")
        print("METHOD 1: Create a .env file in your project root:")
        print('   GEMINI_API_KEY=AIzaSyDAeM-y5isR_bYy5s6zBnkiG9mIRfE6nOI')
        print("\nMETHOD 2: Set environment variable:")
        print('   Windows: set GEMINI_API_KEY=AIzaSyDAeM-y5isR_bYy5s6zBnkiG9mIRfE6nOI')
        
        print("\nGet your free API key from: https://aistudio.google.com/")
        print("="*80)
    
    # Model Configuration - UPDATED FOR GEMINI 3 HACKATHON
    # Use gemini-3-flash-preview for Gemini 3 hackathon
    # Or gemini-2.5-flash for more stability and higher rate limits
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
    
    # Temperature setting
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    
    # API Call Tracking (class variable, not instance)
    _api_call_count = 0
    
    # Generation Config
    GENERATION_CONFIG = {
        "temperature": TEMPERATURE,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
    }
    
    # Safety Settings (permissive for medical content)
    SAFETY_SETTINGS = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    
    @classmethod
    def initialize_gemini(cls):
        """Initialize Gemini API"""
        if not cls.GEMINI_API_KEY:
            raise ValueError(
                "GEMINI_API_KEY not found. Please set it in .env file or environment variables. "
                "Get your key from https://aistudio.google.com/"
            )
        
        try:
            genai.configure(api_key=cls.GEMINI_API_KEY)
            model = genai.GenerativeModel(
                model_name=cls.GEMINI_MODEL,
                generation_config=cls.GENERATION_CONFIG,
                safety_settings=cls.SAFETY_SETTINGS
            )
            print(f"✓ Initialized Gemini model: {cls.GEMINI_MODEL}")
            return model
        except Exception as e:
            print(f"❌ Failed to initialize Gemini: {e}")
            raise
    
    @classmethod
    def increment_api_calls(cls):
        """Track API calls for demonstration purposes"""
        cls._api_call_count += 1
        return cls._api_call_count
    
    @classmethod
    def reset_api_calls(cls):
        """Reset API call counter"""
        cls._api_call_count = 0
    
    @classmethod
    def get_api_call_count(cls):
        """Get current API call count"""
        return cls._api_call_count


# Document type configurations
DOCUMENT_TYPES = [
    'lab_report',
    'visit_note',
    'imaging',
    'specialist_note',
    'discharge_summary'
]

DOCUMENT_TYPE_CONFIG = {
    "lab_report": {
        "keywords": ["laboratory", "lab", "test results", "specimen", "reference range"],
        "priority": "high"
    },
    "visit_note": {
        "keywords": ["chief complaint", "history of present illness", "assessment", "plan"],
        "priority": "high"
    },
    "imaging": {
        "keywords": ["radiology", "CT", "MRI", "X-ray", "ultrasound", "imaging"],
        "priority": "medium"
    },
    "specialist_note": {
        "keywords": ["consultation", "specialist", "cardiology", "nephrology"],
        "priority": "medium"
    },
    "discharge_summary": {
        "keywords": ["discharge", "admission", "hospital course", "emergency"],
        "priority": "high"
    }
}

# ICD-10 Common Codes (for reference)
COMMON_ICD10 = {
    "E11.9": "Type 2 diabetes mellitus without complications",
    "E11.65": "Type 2 diabetes mellitus with hyperglycemia",
    "I10": "Essential (primary) hypertension",
    "E78.5": "Hyperlipidemia, unspecified",
    "E78.0": "Pure hypercholesterolemia",
    "N18.3": "Chronic kidney disease, stage 3 (moderate)",
    "N18.30": "Chronic kidney disease, stage 3 unspecified",
    "I25.10": "Atherosclerotic heart disease of native coronary artery without angina pectoris",
    "Z79.4": "Long term (current) use of insulin",
    "Z79.84": "Long term (current) use of oral hypoglycemic drugs",
    "M79.1": "Myalgia",
    "R07.9": "Chest pain, unspecified"
}

# CPT Codes for Office Visits (Established Patient)
CPT_CODES = {
    "99211": "Office/outpatient visit, established patient, minimal complexity (may not require presence of physician)",
    "99212": "Office/outpatient visit, established patient, straightforward medical decision making",
    "99213": "Office/outpatient visit, established patient, low level of medical decision making",
    "99214": "Office/outpatient visit, established patient, moderate level of medical decision making",
    "99215": "Office/outpatient visit, established patient, high level of medical decision making"
}

# Rate Limits by Model (Requests Per Minute for free tier)
MODEL_RATE_LIMITS = {
    "gemini-3-flash-preview": 10,
    "gemini-3-pro-preview": 2,
    "gemini-2.5-flash": 15,
    "gemini-2.5-pro": 2,
    "gemini-2.0-flash": 15,
    "gemini-2.0-flash-exp": 10,
}

def get_rate_limit_for_model(model_name: str) -> int:
    """
    Get the rate limit for a specific model
    Returns requests per minute (RPM)
    """
    # Remove 'models/' prefix if present
    clean_model = model_name.replace('models/', '')
    
    # Get rate limit, default to conservative 5 RPM if unknown
    return MODEL_RATE_LIMITS.get(clean_model, 5)


# Recommended rate limiter settings based on model
def get_recommended_rate_limiter_settings(model_name: str) -> dict:
    """
    Get recommended rate limiter settings for a model
    Stays under limit for safety (uses 90% of available rate)
    """
    rpm_limit = get_rate_limit_for_model(model_name)
    safe_limit = max(1, int(rpm_limit * 0.9))  # Use 90% of limit
    
    return {
        "max_calls": safe_limit,
        "time_window": 60  # seconds
    }


# Print configuration on import (helpful for debugging)
if __name__ != "__main__":
    if Config.GEMINI_API_KEY:
        rate_settings = get_recommended_rate_limiter_settings(Config.GEMINI_MODEL)
        print(f"✓ Config loaded: Model={Config.GEMINI_MODEL}, Rate Limit={rate_settings['max_calls']}/min")