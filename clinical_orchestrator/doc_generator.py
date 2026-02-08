"""
Documentation Generator - Feature 8: Automated Documentation Assistant
Generates complete SOAP notes and medical coding from brief notes
Optimized for Gemini 3 Flash free tier rate limiting
"""
import asyncio
from typing import Dict, List, Any
import json
from datetime import datetime
import traceback

from config import Config
from document_processor import rate_limiter  # Import shared rate limiter


class DocumentationGenerator:
    """Generates clinical documentation from brief notes"""
    
    def __init__(self):
        self.model = Config.initialize_gemini()
        self.rate_limiter = rate_limiter
    
    async def expand_to_hpi(self, brief_note: str, patient_context: Dict = None) -> str:
        """
        Gemini API Call #10: Expand brief note into complete HPI
        """
        await self.rate_limiter.acquire()
        Config.increment_api_calls()
        
        context_str = ""
        if patient_context:
            context_str = f"\n\nPatient Context:\n{json.dumps(patient_context, indent=2)}"
        
        prompt = f"""You are a medical scribe. Expand this brief clinical note into a complete, professional History of Present Illness (HPI).

Brief Note:
{brief_note}
{context_str}

Create a detailed HPI that includes:
- Complete chronological narrative
- Relevant positives and negatives
- Associated symptoms
- Pertinent past medical history
- Professional medical language

Write 2-3 well-structured paragraphs. Be thorough but concise."""
        
        try:
            print(f"   🔄 Calling Gemini API for HPI...")
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            print(f"   ✓ Gemini response received for HPI")
            return response.text.strip()
        except Exception as e:
            print(f"❌ Error in expand_to_hpi: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            traceback.print_exc()
            return f"Error generating HPI: {str(e)}"
    
    async def generate_objective(self, brief_note: str, vital_signs: Dict = None) -> str:
        """
        Gemini API Call #11: Generate objective findings section
        """
        await self.rate_limiter.acquire()
        Config.increment_api_calls()
        
        vitals_str = ""
        if vital_signs:
            vitals_str = f"\n\nVital Signs:\n{json.dumps(vital_signs, indent=2)}"
        
        prompt = f"""Generate the OBJECTIVE section of a SOAP note for this clinical encounter.

Brief Note:
{brief_note}
{vitals_str}

Include appropriate subsections:
- Vital Signs (if available or typical values)
- Physical Examination findings
- Relevant lab/test results mentioned
- Current medications
- Allergies (if known or state NKDA)

Format as a professional medical note with clear subsections."""
        
        try:
            print(f"   🔄 Calling Gemini API for Objective section...")
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            print(f"   ✓ Gemini response received for Objective")
            return response.text.strip()
        except Exception as e:
            print(f"❌ Error in generate_objective: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            traceback.print_exc()
            return f"Error generating Objective section: {str(e)}"
    
    async def generate_assessment(self, brief_note: str, hpi: str, objective: str) -> str:
        """
        Gemini API Call #12: Create assessment with clinical reasoning
        """
        await self.rate_limiter.acquire()
        Config.increment_api_calls()
        
        prompt = f"""Generate the ASSESSMENT section of a SOAP note with clinical reasoning.

Brief Note:
{brief_note}

HPI:
{hpi}

Objective:
{objective}

Create an assessment that:
1. Lists all active problems/diagnoses
2. Provides clinical reasoning for each
3. Notes stability/changes from baseline
4. Addresses differential diagnoses if relevant

Format as numbered problems with supporting rationale."""
        
        try:
            print(f"   🔄 Calling Gemini API for Assessment...")
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            print(f"   ✓ Gemini response received for Assessment")
            return response.text.strip()
        except Exception as e:
            print(f"❌ Error in generate_assessment: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            traceback.print_exc()
            return f"Error generating Assessment: {str(e)}"
    
    async def generate_plan(self, brief_note: str, assessment: str) -> str:
        """
        Gemini API Call #13: Generate detailed plan with specifics
        """
        await self.rate_limiter.acquire()
        Config.increment_api_calls()
        
        prompt = f"""Generate the PLAN section of a SOAP note.

Brief Note:
{brief_note}

Assessment:
{assessment}

Create a detailed plan organized by problem that includes:
1. Medication changes (start, stop, adjust with specific doses/frequencies)
2. Diagnostic tests ordered
3. Referrals needed (specify specialty)
4. Patient education provided
5. Follow-up schedule (specific timeframe)
6. Return precautions

Be specific with dosages, frequencies, and instructions."""
        
        try:
            print(f"   🔄 Calling Gemini API for Plan...")
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            print(f"   ✓ Gemini response received for Plan")
            return response.text.strip()
        except Exception as e:
            print(f"❌ Error in generate_plan: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            traceback.print_exc()
            return f"Error generating Plan: {str(e)}"
    
    async def extract_icd10_codes(self, soap_note: str) -> List[Dict[str, str]]:
        """
        Gemini API Call #14: Extract ICD-10 diagnosis codes
        """
        await self.rate_limiter.acquire()
        Config.increment_api_calls()
        
        prompt = f"""Extract all appropriate ICD-10 diagnosis codes from this clinical note.

SOAP Note:
{soap_note}

For each diagnosis:
1. Identify the specific ICD-10 code (e.g., E11.9, I10)
2. Provide the full description
3. Indicate if primary or secondary diagnosis

Return a JSON array:
[
    {{
        "code": "ICD-10 code",
        "description": "full description",
        "type": "primary/secondary"
    }}
]

Return ONLY valid JSON array, no other text."""
        
        try:
            print(f"   🔄 Calling Gemini API for ICD-10 codes...")
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            print(f"   ✓ Gemini response received for ICD-10 codes")
            return self._parse_json_array(response.text)
        except Exception as e:
            print(f"❌ Error in extract_icd10_codes: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            traceback.print_exc()
            return [{"code": "Error", "description": f"Failed to extract codes: {str(e)}", "type": "error"}]
    
    async def determine_cpt_code(self, soap_note: str, time_spent: int = None) -> Dict[str, str]:
        """
        Gemini API Call #15: Determine appropriate CPT billing code
        """
        await self.rate_limiter.acquire()
        Config.increment_api_calls()
        
        time_str = f"\nTime spent with patient: {time_spent} minutes" if time_spent else ""
        
        prompt = f"""Determine the most appropriate CPT code for this office visit.

SOAP Note:
{soap_note}
{time_str}

Consider:
- Complexity of medical decision making (MDM)
- Number of problems addressed
- Amount of data reviewed
- Risk of complications/morbidity

CPT Codes (Office/Outpatient Established Patient):
- 99211: Minimal MDM (may not require physician presence)
- 99212: Straightforward MDM (2 of 3: limited problems, limited data, low risk)
- 99213: Low MDM (2 of 3: moderate problems, moderate data, moderate risk)
- 99214: Moderate MDM (2 of 3: multiple problems, extensive data, moderate-high risk)
- 99215: High MDM (2 of 3: extensive problems, extensive data, high risk)

Return a JSON object:
{{
    "cpt_code": "99213",
    "description": "Office visit, moderate complexity",
    "justification": "detailed reasoning for this level including MDM analysis"
}}

Return ONLY valid JSON, no other text."""
        
        try:
            print(f"   🔄 Calling Gemini API for CPT code...")
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            print(f"   ✓ Gemini response received for CPT code")
            return self._parse_json_response(response.text)
        except Exception as e:
            print(f"❌ Error in determine_cpt_code: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            traceback.print_exc()
            return {"cpt_code": "Error", "description": "Failed to determine code", "justification": str(e)}
    
    async def generate_complete_note(self, brief_note: str, patient_context: Dict = None, 
                                    vital_signs: Dict = None, time_spent: int = None) -> Dict[str, Any]:
        """
        Generate complete SOAP note with billing codes
        Total: 6 Gemini API calls (#10-15)
        """
        print("\n📝 Generating complete documentation...")
        
        # Generate SOAP sections sequentially with rate limiting
        print("   ✍️  Expanding to HPI...")
        hpi = await self.expand_to_hpi(brief_note, patient_context)
        print(f"   ✓ HPI generated (Total API calls: {Config.get_api_call_count()})")
        
        print("   📋 Generating Objective section...")
        objective = await self.generate_objective(brief_note, vital_signs)
        print(f"   ✓ Objective section generated (Total API calls: {Config.get_api_call_count()})")
        
        print("   🔍 Creating Assessment...")
        assessment = await self.generate_assessment(brief_note, hpi, objective)
        print(f"   ✓ Assessment generated (Total API calls: {Config.get_api_call_count()})")
        
        print("   📝 Generating Plan...")
        plan = await self.generate_plan(brief_note, assessment)
        print(f"   ✓ Plan generated (Total API calls: {Config.get_api_call_count()})")
        
        # Combine into full SOAP note
        full_soap = f"""SUBJECTIVE:
{hpi}

OBJECTIVE:
{objective}

ASSESSMENT:
{assessment}

PLAN:
{plan}"""
        
        # Extract billing codes
        print("   💰 Extracting ICD-10 codes...")
        icd10_codes = await self.extract_icd10_codes(full_soap)
        print(f"   ✓ ICD-10 codes extracted (Total API calls: {Config.get_api_call_count()})")
        
        print("   💳 Determining CPT code...")
        cpt_code = await self.determine_cpt_code(full_soap, time_spent)
        print(f"   ✓ CPT code determined (Total API calls: {Config.get_api_call_count()})")
        
        print(f"\n✅ Documentation generation complete!\n")
        
        return {
            "soap_note": {
                "subjective": hpi,
                "objective": objective,
                "assessment": assessment,
                "plan": plan,
                "full_note": full_soap
            },
            "billing_codes": {
                "icd10": icd10_codes,
                "cpt": cpt_code
            },
            "metadata": {
                "brief_note": brief_note,
                "generation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "time_spent": time_spent
            }
        }
    
    def format_for_display(self, documentation: Dict[str, Any]) -> str:
        """Format complete documentation for display"""
        soap = documentation['soap_note']
        billing = documentation['billing_codes']
        
        output = f"""
{'='*80}
COMPLETE CLINICAL DOCUMENTATION
{'='*80}

SUBJECTIVE:
{soap['subjective']}

OBJECTIVE:
{soap['objective']}

ASSESSMENT:
{soap['assessment']}

PLAN:
{soap['plan']}

{'='*80}
BILLING CODES
{'='*80}

ICD-10 DIAGNOSIS CODES:
"""
        for code in billing.get('icd10', []):
            output += f"  • {code.get('code', 'N/A')}: {code.get('description', 'N/A')} ({code.get('type', 'N/A')})\n"
        
        cpt = billing.get('cpt', {})
        output += f"""
CPT PROCEDURE CODE:
  • {cpt.get('cpt_code', 'N/A')}: {cpt.get('description', 'N/A')}
  
JUSTIFICATION:
  {cpt.get('justification', 'N/A')}

{'='*80}
"""
        return output
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON object from Gemini response"""
        try:
            json_text = response_text.strip()
            if json_text.startswith("```json"):
                json_text = json_text[7:]
            if json_text.startswith("```"):
                json_text = json_text[3:]
            if json_text.endswith("```"):
                json_text = json_text[:-3]
            json_text = json_text.strip()
            
            return json.loads(json_text)
        except Exception as e:
            print(f"⚠️  JSON parsing warning: {str(e)}")
            return {"error": f"Failed to parse JSON: {str(e)}", "raw": response_text[:200]}
    
    def _parse_json_array(self, response_text: str) -> List[Dict[str, Any]]:
        """Parse JSON array from Gemini response"""
        try:
            json_text = response_text.strip()
            if json_text.startswith("```json"):
                json_text = json_text[7:]
            if json_text.startswith("```"):
                json_text = json_text[3:]
            if json_text.endswith("```"):
                json_text = json_text[:-3]
            json_text = json_text.strip()
            
            result = json.loads(json_text)
            return result if isinstance(result, list) else []
        except Exception as e:
            print(f"⚠️  JSON array parsing warning: {str(e)}")
            return [{"error": f"Failed to parse JSON: {str(e)}", "raw": response_text[:200]}]