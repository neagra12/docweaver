"""
Temporal Analyzer - Feature 2: Multi-Source Data Fusion
Performs temporal reasoning, trend detection, and causal analysis
Gemini API Calls #6-9
Optimized for Gemini 3 Flash free tier rate limiting
"""
import asyncio
from typing import Dict, List, Any
import json

from config import Config
from document_processor import rate_limiter


class TemporalAnalyzer:
    """Analyzes temporal relationships and causality in medical data"""
    
    def __init__(self):
        self.model = Config.initialize_gemini()
        self.rate_limiter = rate_limiter
    
    async def identify_new_events(self, documents: List[Dict[str, Any]], last_visit_date: str = None) -> Dict[str, Any]:
        """
        Gemini API Call #6: Identify new events since last visit
        """
        await self.rate_limiter.acquire()
        Config.increment_api_calls()
        
        doc_summary = self._prepare_document_summary(documents)
        
        prompt = f"""Analyze these medical documents and identify NEW events since the last visit.

Last Visit Date: {last_visit_date or "3 months ago"}

Documents:
{doc_summary}

Identify:
1. New diagnoses or conditions
2. New abnormal test results
3. ER visits or hospitalizations
4. New medications started or stopped
5. New specialist consultations

Return a JSON object:
{{
    "new_events": [
        {{
            "event": "description",
            "date": "YYYY-MM-DD",
            "severity": "critical/urgent/routine",
            "source_document": "document name"
        }}
    ]
}}

Return ONLY valid JSON, no other text."""
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            return self._parse_json_response(response.text)
        except Exception as e:
            print(f"❌ Error in identify_new_events: {str(e)}")
            return {"new_events": [], "error": str(e)}
    
    async def detect_lab_trends(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Gemini API Call #7: Detect trends in lab values over time
        """
        # Extract all lab data
        lab_data = []
        for doc in documents:
            if doc.get('document_type') == 'lab_report':
                extracted = doc.get('extracted_data', {})
                if 'error' not in extracted:
                    lab_data.append({
                        'date': extracted.get('test_date'),
                        'tests': extracted.get('tests', [])
                    })
        
        if not lab_data:
            return {"trends": [], "message": "No lab data available"}
        
        await self.rate_limiter.acquire()
        Config.increment_api_calls()
        
        prompt = f"""Analyze these lab results over time and identify important trends.

Lab Results (chronological):
{json.dumps(lab_data, indent=2)}

For each test showing a trend:
1. Identify the test name
2. Describe the trend (improving/worsening/stable)
3. Assess clinical significance
4. Note if values are moving out of normal range

Return a JSON object:
{{
    "trends": [
        {{
            "test_name": "name",
            "direction": "improving/worsening/stable",
            "values_over_time": ["oldest", "recent"],
            "clinical_significance": "high/medium/low",
            "interpretation": "what this means clinically"
        }}
    ]
}}

Return ONLY valid JSON, no other text."""
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            return self._parse_json_response(response.text)
        except Exception as e:
            print(f"❌ Error in detect_lab_trends: {str(e)}")
            return {"trends": [], "error": str(e)}
    
    async def establish_causal_relationships(self, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Gemini API Call #8: Establish causal relationships between events
        
        THIS IS THE KEY DIFFERENTIATOR - Temporal causality detection
        "Event A led to Event B" - proves sophisticated reasoning
        """
        await self.rate_limiter.acquire()
        Config.increment_api_calls()
        
        events = self._extract_all_events(documents)
        
        # If no events extracted, return empty
        if not events:
            return {
                "causal_links": [],
                "summary": "Insufficient data to establish causal relationships"
            }
        
        prompt = f"""Analyze these chronological medical events and identify CAUSAL RELATIONSHIPS.

Events (chronological order):
{json.dumps(events, indent=2)}

Look for:
1. Drug-drug interactions (e.g., NSAID + ACE inhibitor → kidney function change)
2. Treatment effects (medication → lab value changes)
3. Disease progression
4. Side effects from medications
5. Complications from procedures

For each causal relationship:
- Identify Event A (cause)
- Identify Event B (effect)
- Explain the mechanism (HOW A led to B)
- Assess confidence level
- Rate clinical importance

Return a JSON object:
{{
    "causal_links": [
        {{
            "cause_event": "Event A description and date",
            "effect_event": "Event B description and date",
            "mechanism": "detailed explanation of how A led to B",
            "confidence": "high/medium/low",
            "clinical_importance": "critical/important/notable",
            "recommendation": "what action should be taken"
        }}
    ],
    "summary": "overall narrative of patient's clinical course"
}}

Return ONLY valid JSON, no other text."""
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            return self._parse_json_response(response.text)
        except Exception as e:
            print(f"❌ Error in establish_causal_relationships: {str(e)}")
            return {"causal_links": [], "summary": "Error analyzing causality", "error": str(e)}
    
    async def prioritize_changes(self, new_events: Dict, trends: Dict, causal_links: Dict) -> Dict[str, Any]:
        """
        Gemini API Call #9: Prioritize and categorize all changes
        """
        await self.rate_limiter.acquire()
        Config.increment_api_calls()
        
        combined_data = {
            "new_events": new_events,
            "trends": trends,
            "causal_links": causal_links
        }
        
        prompt = f"""Review all clinical changes and prioritize them for physician review.

Data:
{json.dumps(combined_data, indent=2)}

Categorize each finding:
- CRITICAL: Requires immediate attention (life-threatening, severe deterioration)
- URGENT: Needs attention soon (significant changes, new concerning findings)
- ROUTINE: Monitor at next visit (stable, expected changes)

Return a JSON object:
{{
    "critical": [
        {{
            "finding": "description",
            "rationale": "why this is critical",
            "suggested_action": "what to do immediately"
        }}
    ],
    "urgent": [
        {{
            "finding": "description",
            "rationale": "why this needs attention",
            "suggested_action": "what to do soon"
        }}
    ],
    "routine": [
        {{
            "finding": "description",
            "rationale": "why this is routine"
        }}
    ]
}}

Return ONLY valid JSON, no other text."""
        
        try:
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            return self._parse_json_response(response.text)
        except Exception as e:
            print(f"❌ Error in prioritize_changes: {str(e)}")
            return {"critical": [], "urgent": [], "routine": [], "error": str(e)}
    
    async def create_timeline(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create a visual timeline of all events (no API call - just data organization)
        """
        timeline = []
        
        for doc in documents:
            doc_type = doc.get('document_type', '')
            extracted = doc.get('extracted_data', {})
            
            # Skip documents with errors
            if 'error' in extracted:
                continue
            
            # Extract date and event based on document type
            date = None
            event = None
            
            if doc_type == 'lab_report':
                date = extracted.get('test_date')
                tests = extracted.get('tests', [])
                event = f"Lab Tests: {len(tests)} tests performed"
            elif doc_type == 'visit_note':
                date = extracted.get('visit_date')
                event = f"Office Visit: {extracted.get('chief_complaint', 'Follow-up')}"
            elif doc_type == 'imaging':
                date = extracted.get('exam_date')
                event = f"Imaging: {extracted.get('modality', '')} {extracted.get('body_part', '')}"
            elif doc_type == 'specialist_note':
                date = extracted.get('consultation_date')
                event = f"Specialist: {extracted.get('specialty', '')} consultation"
            elif doc_type == 'discharge_summary':
                date = extracted.get('visit_date')
                event = "Emergency Department Visit"
            
            if date and event:
                timeline.append({
                    "date": date,
                    "event": event,
                    "document_type": doc_type,
                    "document_name": doc.get('file_name', '')
                })
        
        # Sort by date, handling None values
        timeline.sort(key=lambda x: x.get('date') or '9999-12-31')
        
        return timeline
    
    async def analyze_all(self, documents: List[Dict[str, Any]], last_visit_date: str = None) -> Dict[str, Any]:
        """
        Run complete temporal analysis pipeline
        Total: 4 Gemini API calls (#6, #7, #8, #9)
        """
        print("\n🧠 Running temporal analysis...")
        
        # Run all analyses
        print("   🔍 Identifying new events...")
        new_events = await self.identify_new_events(documents, last_visit_date)
        print(f"   ✓ New events identified (Total API calls: {Config.get_api_call_count()})")
        
        print("   📊 Detecting lab trends...")
        trends = await self.detect_lab_trends(documents)
        print(f"   ✓ Lab trends detected (Total API calls: {Config.get_api_call_count()})")
        
        print("   🔗 Establishing causal relationships...")
        causal_links = await self.establish_causal_relationships(documents)
        print(f"   ✓ Causal relationships established (Total API calls: {Config.get_api_call_count()})")
        
        print("   ⚖️  Prioritizing changes...")
        priorities = await self.prioritize_changes(new_events, trends, causal_links)
        print(f"   ✓ Changes prioritized (Total API calls: {Config.get_api_call_count()})")
        
        print("   📅 Creating timeline...")
        timeline = await self.create_timeline(documents)
        print(f"   ✓ Timeline created")
        
        print(f"✅ Temporal analysis complete!\n")
        
        return {
            "new_events": new_events,
            "trends": trends,
            "causal_analysis": causal_links,
            "priorities": priorities,
            "timeline": timeline
        }
    
    def _prepare_document_summary(self, documents: List[Dict[str, Any]]) -> str:
        """Prepare a concise summary of all documents"""
        summary = []
        for doc in documents:
            doc_type = doc.get('document_type', 'unknown')
            file_name = doc.get('file_name', 'unknown')
            extracted = doc.get('extracted_data', {})
            
            # Skip documents with errors
            if 'error' in extracted:
                continue
            
            date = extracted.get('test_date') or \
                   extracted.get('visit_date') or \
                   extracted.get('exam_date') or \
                   extracted.get('consultation_date') or "Unknown date"
            summary.append(f"- {file_name} ({doc_type}, {date})")
        return "\n".join(summary) if summary else "No valid documents found"
    
    def _extract_all_events(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract all events from documents in chronological order"""
        events = []
        
        for doc in documents:
            doc_type = doc.get('document_type', '')
            extracted = doc.get('extracted_data', {})
            
            # Skip documents with errors
            if 'error' in extracted:
                continue
            
            if doc_type == 'lab_report':
                date = extracted.get('test_date')
                tests = extracted.get('tests', [])
                for test in tests:
                    if isinstance(test, dict):  # Ensure test is a dictionary
                        events.append({
                            "date": date or 'Unknown',
                            "type": "lab_result",
                            "description": f"{test.get('name', 'Unknown test')}: {test.get('value', '')} {test.get('unit', '')} ({test.get('flag', 'NORMAL')})"
                        })
            
            elif doc_type == 'visit_note':
                date = extracted.get('visit_date')
                events.append({
                    "date": date or 'Unknown',
                    "type": "office_visit",
                    "description": f"Visit: {extracted.get('chief_complaint', 'Follow-up')}"
                })
                
                # Add medications as events
                medications = extracted.get('medications', [])
                if isinstance(medications, list):
                    for med in medications:
                        if med:  # Check if med is not empty
                            events.append({
                                "date": date or 'Unknown',
                                "type": "medication",
                                "description": f"Medication prescribed: {med}"
                            })
            
            elif doc_type == 'discharge_summary':
                date = extracted.get('visit_date')
                events.append({
                    "date": date or 'Unknown',
                    "type": "emergency_visit",
                    "description": f"ER visit: {extracted.get('chief_complaint', 'Emergency')}"
                })
            
            elif doc_type == 'specialist_note':
                date = extracted.get('consultation_date')
                events.append({
                    "date": date or 'Unknown',
                    "type": "specialist_consult",
                    "description": f"{extracted.get('specialty', 'Specialist')} consultation: {extracted.get('reason_for_consult', 'Consultation')}"
                })
        
        # Sort by date, with proper handling of None/Unknown values
        events.sort(key=lambda x: x.get('date') if x.get('date') and x.get('date') != 'Unknown' else '9999-12-31')
        
        return events
    
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