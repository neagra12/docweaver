"""
FastAPI Backend for DocWeaver Frontend Integration
Provides RESTful API endpoints for the Next.js frontend
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
import os
import tempfile
import asyncio
from datetime import datetime
import traceback

from orchestrator import DocWeaverOrchestrator
from document_processor import extract_text_from_file
from config import Config

app = FastAPI(
    title="DocWeaver API",
    description="Clinical Intelligence Platform API powered by Gemini 3",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "https://your-vercel-app.vercel.app"  # Add your Vercel URL here
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = DocWeaverOrchestrator()


# API Endpoints

@app.get("/")
async def root():
    """Root endpoint - Health check"""
    return {
        "status": "healthy",
        "service": "DocWeaver API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat(),
        "model": Config.GEMINI_MODEL,
        "docs": "/docs"
    }


@app.get("/api/health")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "model": Config.GEMINI_MODEL,
        "api_key_configured": bool(Config.GEMINI_API_KEY),
        "total_api_calls": Config.get_api_call_count()
    }


@app.post("/api/workflow/complete")
async def complete_workflow(files: List[UploadFile] = File(...)):
    """
    Complete workflow: Process documents + generate documentation + coordinate care
    This is the main endpoint the frontend uses
    """
    try:
        print(f"\n{'='*80}")
        print(f"🚀 COMPLETE WORKFLOW STARTED")
        print(f"{'='*80}")
        print(f"Files received: {len(files)}")
        for file in files:
            print(f"  - {file.filename} ({file.content_type})")
        
        # Save uploaded files temporarily
        temp_files = []
        for file in files:
            suffix = os.path.splitext(file.filename)[1] or '.txt'
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode='wb') as temp_file:
                content = await file.read()
                temp_file.write(content)
                temp_files.append(temp_file.name)
                print(f"  ✓ Saved: {file.filename} -> {temp_file.name}")
        
        # Default brief note for documentation generation
        brief_note = "Patient follow-up visit. Review recent test results and clinical data. Update treatment plan based on findings."
        
        print(f"\n📊 Processing workflow...")
        
        # Run complete workflow
        results = await orchestrator.run_complete_workflow(temp_files, brief_note)
        
        # Clean up temp files
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except Exception as e:
                print(f"  ⚠️  Could not delete temp file: {e}")
        
        print(f"\n{'='*80}")
        print(f"✅ WORKFLOW COMPLETE")
        print(f"{'='*80}")
        print(f"Total API calls: {results['summary']['total_api_calls']}")
        print(f"Processing time: {results['summary']['processing_time_seconds']:.1f}s")
        print(f"Documents: {results['summary']['documents_processed']}")
        print(f"Actions: {results['summary']['actions_automated']}")
        print(f"{'='*80}\n")
        
        return JSONResponse(content=results)
    
    except Exception as e:
        print(f"\n{'='*80}")
        print(f"❌ ERROR IN WORKFLOW")
        print(f"{'='*80}")
        print(f"Error: {str(e)}")
        traceback.print_exc()
        print(f"{'='*80}\n")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/workflow/documents")
async def process_documents(files: List[UploadFile] = File(...)):
    """
    Feature 2: Multi-Source Data Fusion
    Process multiple documents and perform temporal analysis
    """
    try:
        print(f"\n📊 Processing {len(files)} documents for data fusion")
        
        if not files:
            raise HTTPException(status_code=400, detail="No files provided")
        
        # Save uploaded files temporarily
        temp_files = []
        for file in files:
            suffix = os.path.splitext(file.filename)[1] or '.txt'
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, mode='wb') as temp_file:
                content = await file.read()
                temp_file.write(content)
                temp_files.append(temp_file.name)
        
        # Process documents
        result = await orchestrator.process_patient_documents(temp_files)
        
        # Clean up temp files
        for temp_file in temp_files:
            try:
                os.unlink(temp_file)
            except:
                pass
        
        print(f"✅ Documents processed! API calls: {result['api_calls_used']}")
        
        return JSONResponse(content=result)
    
    except Exception as e:
        print(f"❌ Error in process_documents: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/documentation/generate")
async def generate_documentation(brief_note: str = Form(...)):
    """
    Feature 8: Smart Documentation
    Generate complete SOAP note from brief note
    """
    try:
        print(f"\n📝 Generating documentation")
        print(f"Brief note: {brief_note[:100]}...")
        
        if not brief_note or len(brief_note.strip()) == 0:
            raise HTTPException(status_code=400, detail="Brief note is required")
        
        # Patient context (default)
        patient_context = {
            "name": "Patient",
            "dob": "01/01/1970",
            "mrn": "12345678",
            "diagnoses": []
        }
        
        # Generate documentation
        result = await orchestrator.generate_clinical_documentation(
            brief_note,
            patient_context
        )
        
        print(f"✅ Documentation generated! API calls: {result['api_calls_used']}")
        
        return JSONResponse(content=result)
    
    except Exception as e:
        print(f"❌ Error in generate_documentation: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/coordination/generate")
async def generate_coordination():
    """
    Feature 9: Care Coordination
    Generate care coordination actions based on previous analysis
    """
    try:
        print(f"\n🔗 Generating care coordination")
        
        # Check if we have prerequisite data
        if not orchestrator.analysis_results:
            raise HTTPException(
                status_code=400,
                detail="Please process documents first (Feature 2)"
            )
        
        if not orchestrator.documentation_results:
            raise HTTPException(
                status_code=400,
                detail="Please generate documentation first (Feature 8)"
            )
        
        # Coordinate care
        result = await orchestrator.coordinate_care()
        
        print(f"✅ Coordination complete! API calls: {result['api_calls_used']}")
        
        return JSONResponse(content=result)
    
    except Exception as e:
        print(f"❌ Error in generate_coordination: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/demo/run")
async def run_demo():
    """
    Run the complete demo workflow with Sarah Chen data
    """
    try:
        print(f"\n🎬 Running demo workflow")
        
        demo_files = [
            "demo_data/sarah_chen_lab_6months.txt",
            "demo_data/sarah_chen_lab_recent.txt",
            "demo_data/sarah_chen_er_discharge.txt",
            "demo_data/sarah_chen_cardiology_consult.txt",
            "demo_data/sarah_chen_last_visit.txt"
        ]
        
        # Check if demo files exist
        for file in demo_files:
            if not os.path.exists(file):
                raise HTTPException(
                    status_code=404,
                    detail=f"Demo file not found: {file}. Please ensure demo_data folder exists."
                )
        
        brief_note = "52F DM2 f/u, ER visit for CP ruled out, D/C ibuprofen due to kidney concerns, start atorvastatin 20mg for LDL 145, increase lisinopril to 40mg, A1C up to 6.8%, new microalbuminuria 35, refer ophthalmology"
        
        # Run complete workflow
        results = await orchestrator.run_complete_workflow(demo_files, brief_note)
        
        print(f"✅ Demo complete! API calls: {results['summary']['total_api_calls']}")
        
        return JSONResponse(content=results)
    
    except Exception as e:
        print(f"❌ Error in run_demo: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/demo/files")
async def get_demo_files():
    """
    Get list of available demo data files
    """
    try:
        demo_dir = "demo_data"
        if not os.path.exists(demo_dir):
            return {
                "status": "success",
                "files": [],
                "message": "Demo data directory not found"
            }
        
        files = [f for f in os.listdir(demo_dir) if f.endswith(('.txt', '.pdf', '.docx'))]
        return {
            "status": "success",
            "files": files,
            "count": len(files),
            "message": f"Found {len(files)} demo files"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/metrics")
async def get_metrics():
    """
    Get current API usage statistics
    """
    try:
        return {
            "status": "success",
            "total_api_calls": Config.get_api_call_count(),
            "model": Config.GEMINI_MODEL,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/reset")
async def reset_session():
    """
    Reset the orchestrator session (for testing)
    """
    global orchestrator
    orchestrator = DocWeaverOrchestrator()
    Config.reset_api_calls()
    
    return {
        "status": "success",
        "message": "Session reset successfully",
        "api_calls": Config.get_api_call_count()
    }


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*80)
    print("🏥 DocWeaver API Server")
    print("="*80)
    print(f"\n📋 Configuration:")
    print(f"   Model: {Config.GEMINI_MODEL}")
    print(f"   API Key: {'✓ Configured' if Config.GEMINI_API_KEY else '✗ Not configured'}")
    print(f"\n📍 Server Endpoints:")
    print(f"   Local: http://localhost:8000")
    print(f"   Health: http://localhost:8000/api/health")
    print(f"   Docs: http://localhost:8000/docs")
    print(f"   Interactive API: http://localhost:8000/redoc")
    print(f"\n💡 Frontend Connection:")
    print(f"   Set NEXT_PUBLIC_API_URL=http://localhost:8000")
    print(f"\n🚀 Starting server...")
    print("="*80 + "\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )