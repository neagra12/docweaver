"""
Care Coordination Agent - Feature 9: Care Coordination Automation
Autonomously generates referrals, follow-ups, and patient communications
Optimized for Gemini 3 Flash free tier rate limiting
"""
import asyncio
from typing import Dict, List, Any
import json
from datetime import datetime, timedelta
import traceback

from config import Config
from document_processor import rate_limiter  # Import shared rate limiter


class CareCoordinationAgent:
    """Autonomously coordinates care based on clinical analysis"""
    
    def __init__(self):
        self.model = Config.initialize_gemini()
        self.rate_limiter = rate_limiter
    
    async def identify_coordination_needs(self, analysis_results: Dict[str, Any], 
                                         soap_note: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Gemini API Call #16: Identify all coordination actions needed
        """
        await self.rate_limiter.acquire()
        Config.increment_api_calls()
        
        # Combine temporal analysis and SOAP note
        combined_data = {
            "temporal_analysis": analysis_results,
            "soap_note": soap_note.get('soap_note', {}) if soap_note else {}
        }
        
        prompt = f"""Analyze this clinical data and identify ALL care coordination actions needed.

Clinical Data:
{json.dumps(combined_data, indent=2)}

Identify:
1. REFERRALS: Any specialist consultations mentioned or needed
2. FOLLOW-UPS: When patient needs to return (based on plan or severity)
3. ORDERS: Labs, imaging, or tests that need scheduling
4. PATIENT COMMUNICATIONS: Visit summaries, medication changes, instructions

Return a JSON object:
{{
    "referrals": [
        {{
            "specialty": "specialty type",
            "reason": "reason for referral",
            "urgency": "urgent/routine",
            "notes": "additional context"
        }}
    ],
    "follow_ups": [
        {{
            "timeframe": "e.g., 3 months",
            "reason": "reason for follow-up",
            "required_prep": "e.g., fasting labs"
        }}
    ],
    "orders": [
        {{
            "type": "lab/imaging/test",
            "description": "what to order",
            "timing": "when to complete"
        }}
    ],
    "patient_communication_needed": true/false
}}

Return ONLY valid JSON, no other text."""
        
        try:
            print(f"   🔄 Calling Gemini API for coordination needs...")
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            print(f"   ✓ Gemini response received for coordination needs")
            return self._parse_json_response(response.text)
        except Exception as e:
            print(f"❌ Error in identify_coordination_needs: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            traceback.print_exc()
            return {
                "referrals": [],
                "follow_ups": [],
                "orders": [],
                "patient_communication_needed": False,
                "error": str(e)
            }
    
    async def generate_referral_letter(self, referral: Dict[str, Any], 
                                      patient_context: Dict[str, Any]) -> str:
        """
        Gemini API Call #17: Generate professional referral letter
        """
        await self.rate_limiter.acquire()
        Config.increment_api_calls()
        
        prompt = f"""Generate a professional specialist referral letter.

Referral Details:
{json.dumps(referral, indent=2)}

Patient Context:
{json.dumps(patient_context, indent=2)}

Create a referral letter that includes:
1. Patient demographics (name, DOB, MRN from context)
2. Reason for referral
3. Relevant medical history
4. Pertinent test results
5. Current medications
6. Specific questions for specialist
7. Professional closing

Format as a formal medical referral letter."""
        
        try:
            print(f"   🔄 Calling Gemini API for referral letter...")
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            print(f"   ✓ Gemini response received for referral letter")
            return response.text.strip()
        except Exception as e:
            print(f"❌ Error in generate_referral_letter: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            traceback.print_exc()
            return f"Error generating referral letter: {str(e)}"
    
    async def generate_doctor_handover_report(self, analysis_results: Dict[str, Any], 
                                            soap_note: Dict[str, Any] = None,
                                            patient_context: Dict[str, Any] = None) -> str:
        """
        Gemini API Call #19: Generate a high-level handover report for the next doctor
        """
        await self.rate_limiter.acquire()
        Config.increment_api_calls()
        
        prompt = f"""Generate a detailed 1-page Clinical Handover Report for a receiving physician.
        
        Clinical Information:
        Temporal Analysis: {json.dumps(analysis_results, indent=2)}
        SOAP Note: {json.dumps(soap_note, indent=2) if soap_note else 'N/A'}
        Patient Context: {json.dumps(patient_context, indent=2)}
        
        The report should be structured for a doctor to review IN PRIOR to a patient visit.
        Include these sections:
        1. CLINICAL SUMMARY: High-level overview of patient status
        2. CRITICAL FINDINGS: Any urgent issues or lab trends discovered
        3. ACTIVE MEDICAL PROBLEMS: Sorted by priority
        4. CURRENT TREATMENT PLAN & RECENT CHANGES
        5. PENDING ACTIONS & COORDINATION: Referrals, labs, or follow-ups needed
        6. KEY QUESTIONS FOR THE NEXT VISIT
        
        Tone should be professional, concise, and clinically focused. Use medical terminology.
        Format it as a clean, professional clinical report."""
        
        try:
            print(f"   🔄 Calling Gemini API for doctor handover report...")
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            print(f"   ✓ Gemini response received for handover report")
            return response.text.strip()
        except Exception as e:
            print(f"❌ Error in generate_doctor_handover_report: {str(e)}")
            traceback.print_exc()
            return f"Error generating clinical handover report: {str(e)}"

    async def generate_patient_communication(self, visit_summary: Dict[str, Any], 
                                            patient_level: str = "general") -> str:
        """
        Gemini API Call #18: Generate patient-friendly communication
        """
        await self.rate_limiter.acquire()
        Config.increment_api_calls()
        
        prompt = f"""Create a patient-friendly visit summary and after-visit instructions.

Visit Information:
{json.dumps(visit_summary, indent=2)}

Patient Reading Level: {patient_level}

Create a communication that:
1. Summarizes what was discussed in simple terms
2. Explains diagnoses in plain language (avoid medical jargon)
3. Lists medication changes with clear instructions
4. Provides specific action items for the patient
5. Explains when to call doctor or return
6. Uses encouraging, supportive tone

Format as a clear, easy-to-read document suitable for patient portal."""
        
        try:
            print(f"   🔄 Calling Gemini API for patient communication...")
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            print(f"   ✓ Gemini response received for patient communication")
            return response.text.strip()
        except Exception as e:
            print(f"❌ Error in generate_patient_communication: {str(e)}")
            print(f"   Error type: {type(e).__name__}")
            traceback.print_exc()
            return f"Error generating patient communication: {str(e)}"
    
    async def coordinate_all_actions(self, analysis_results: Dict[str, Any],
                                    soap_note: Dict[str, Any] = None,
                                    patient_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Run complete care coordination pipeline
        Total: 3+ Gemini API calls (#16, #17, #18+)
        """
        print("\n🔗 Running care coordination automation...")
        
        # Identify what needs to be coordinated
        print("   🔍 Identifying coordination needs...")
        coordination_needs = await self.identify_coordination_needs(analysis_results, soap_note)
        print(f"   ✓ Coordination needs identified (Total API calls: {Config.get_api_call_count()})")
        
        # Generate referral letters for each referral
        referral_letters = []
        referrals = coordination_needs.get('referrals', [])
        for i, referral in enumerate(referrals):
            print(f"   📨 Generating referral letter {i+1}/{len(referrals)} for {referral.get('specialty', 'Unknown')}...")
            letter = await self.generate_referral_letter(referral, patient_context or {})
            referral_letters.append({
                "specialty": referral.get('specialty'),
                "reason": referral.get('reason'),
                "urgency": referral.get('urgency'),
                "letter": letter
            })
            print(f"   ✓ Referral letter generated (Total API calls: {Config.get_api_call_count()})")
        
        # Generate patient communication if needed
        patient_communication = None
        if coordination_needs.get('patient_communication_needed'):
            print("   💬 Generating patient communication...")
            visit_summary = {
                "diagnoses": soap_note.get('soap_note', {}).get('assessment', '') if soap_note else '',
                "plan": soap_note.get('soap_note', {}).get('plan', '') if soap_note else '',
                "follow_ups": coordination_needs.get('follow_ups', []),
                "new_medications": self._extract_medications_from_plan(
                    soap_note.get('soap_note', {}).get('plan', '') if soap_note else ''
                )
            }
            patient_communication = await self.generate_patient_communication(visit_summary)
            print(f"   ✓ Patient communication generated (Total API calls: {Config.get_api_call_count()})")
        
        # New Feature: Generate Doctor Handover Report
        print("   🩺 Generating doctor handover report...")
        handover_report = await self.generate_doctor_handover_report(
            analysis_results, 
            soap_note, 
            patient_context
        )
        print(f"   ✓ Doctor handover report generated (Total API calls: {Config.get_api_call_count()})")
        
        print(f"\n✅ Care coordination complete!\n")
        
        return {
            "coordination_needs": coordination_needs,
            "referrals": referral_letters,
            "follow_ups": coordination_needs.get('follow_ups', []),
            "orders": coordination_needs.get('orders', []),
            "patient_communication": patient_communication,
            "handover_report": handover_report,
            "actions_count": len(referral_letters) + len(coordination_needs.get('follow_ups', [])) + 
                           len(coordination_needs.get('orders', []))
        }
    
    def format_coordination_summary(self, coordination: Dict[str, Any]) -> str:
        """Format coordination results for display"""
        output = f"""
{'='*80}
CARE COORDINATION ACTIONS
{'='*80}

TOTAL ACTIONS AUTOMATED: {coordination.get('actions_count', 0)}

"""
        # Referrals
        referrals = coordination.get('referrals', [])
        if referrals:
            output += f"""REFERRALS NEEDED: {len(referrals)}
"""
            for i, ref in enumerate(referrals, 1):
                output += f"""
{i}. {ref.get('specialty', 'N/A')} - {ref.get('urgency', 'routine').upper()}
   Reason: {ref.get('reason', 'N/A')}
   
   REFERRAL LETTER:
   {'-'*70}
{ref.get('letter', 'N/A')}
   {'-'*70}
"""
        
        # Follow-ups
        follow_ups = coordination.get('follow_ups', [])
        if follow_ups:
            output += f"""
FOLLOW-UP APPOINTMENTS: {len(follow_ups)}
"""
            for i, fu in enumerate(follow_ups, 1):
                output += f"""
{i}. Timeframe: {fu.get('timeframe', 'N/A')}
   Reason: {fu.get('reason', 'N/A')}
   Prep Required: {fu.get('required_prep', 'None')}
"""
        
        # Orders
        orders = coordination.get('orders', [])
        if orders:
            output += f"""
ORDERS TO PLACE: {len(orders)}
"""
            for i, order in enumerate(orders, 1):
                output += f"""
{i}. Type: {order.get('type', 'N/A')}
   Description: {order.get('description', 'N/A')}
   Timing: {order.get('timing', 'N/A')}
"""
        
        # Patient Communication
        patient_comm = coordination.get('patient_communication')
        if patient_comm:
            output += f"""
PATIENT COMMUNICATION:
{'-'*70}
{patient_comm}
{'-'*70}
"""
        
        output += f"""
{'='*80}
"""
        return output
    
    def _extract_medications_from_plan(self, plan_text: str) -> List[str]:
        """Simple extraction of medications from plan text"""
        medications = []
        lines = plan_text.split('\n')
        for line in lines:
            if any(keyword in line.lower() for keyword in ['start', 'prescribe', 'begin', 'initiate']):
                medications.append(line.strip())
        return medications
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """Parse JSON from Gemini response"""
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