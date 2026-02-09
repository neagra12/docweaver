"""
DocWeaver - Modern Clinical Intelligence Platform
Inspired by leading healthcare software design
"""
import streamlit as st
import asyncio
import json
from datetime import datetime
import os
import traceback
import plotly.graph_objects as go
import plotly.express as px
from config import Config
from orchestrator import DocWeaverOrchestrator
from document_processor import extract_text_from_file


# Page configuration
st.set_page_config(
    page_title="DocWeaver - Clinical Intelligence Platform",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern Healthcare CSS - Inspired by Ensora Health
st.markdown("""
<style>
    /* Import Modern Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }
    
    /* Modern Header with Gradient Background */
    .hero-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #172554 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: #94a3b8;
        font-weight: 400;
    }
    
    .hero-badge {
        display: inline-block;
        background: rgba(59, 130, 246, 0.2);
        color: #60a5fa;
        padding: 0.5rem 1.25rem;
        border-radius: 20px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-top: 1rem;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    /* Feature Cards - Modern Design */
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        border: 1px solid #f1f5f9;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card:before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%);
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
    }
    
    .feature-card:hover:before {
        transform: scaleX(1);
    }
    
    .feature-icon {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.75rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.3);
    }
    
    .feature-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.5rem;
    }
    
    .feature-subtitle {
        font-size: 1rem;
        color: #64748b;
        margin-bottom: 1.5rem;
        font-weight: 500;
    }
    
    .feature-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .feature-list li {
        padding: 0.75rem 0;
        color: #475569;
        font-size: 0.95rem;
        display: flex;
        align-items: center;
    }
    
    .feature-list li:before {
        content: "✓";
        color: #10b981;
        font-weight: 700;
        font-size: 1.1rem;
        margin-right: 0.75rem;
        flex-shrink: 0;
    }
    
    /* Demo Section - Eye-catching */
    .demo-section {
        background: linear-gradient(135deg, #0ea5e9 0%, #2563eb 100%);
        border-radius: 20px;
        padding: 3rem;
        margin: 2rem 0;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
    }
    
    .demo-title {
        font-size: 2rem;
        font-weight: 800;
        color: white;
        margin-bottom: 0.75rem;
    }
    
    .demo-subtitle {
        font-size: 1.125rem;
        color: rgba(255, 255, 255, 0.9);
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    .demo-list {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .demo-list li {
        color: white;
        padding: 0.75rem 0;
        font-size: 1rem;
        display: flex;
        align-items: flex-start;
    }
    
    .demo-list li:before {
        content: "→";
        margin-right: 1rem;
        font-weight: 700;
        flex-shrink: 0;
    }
    
    /* Sidebar - Modern Redesign (Professional Medical Light Theme) */
    [data-testid="stSidebar"] {
        background: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 2rem 1.5rem;
    }
    
    .sidebar-logo {
        font-size: 1.75rem;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 2rem;
        text-align: center;
        letter-spacing: -0.5px;
    }
    
    .sidebar-logo-accent {
        color: #3b82f6;
    }
    
    /* Radio Buttons - Clean Lines */
    .stRadio > div {
        gap: 0.5rem;
    }
    
    .stRadio > div > label {
        background: transparent;
        border: 1px solid transparent;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        color: #475569;
        font-weight: 600;
        transition: all 0.2s ease;
        cursor: pointer;
        display: flex;
        align-items: center;
    }
    
    .stRadio > div > label:hover {
        background: #f1f5f9;
        color: #0f172a;
    }
    
    .stRadio > div > label[data-checked="true"] {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        color: #1e40af;
        font-weight: 700;
    }
    
    /* Sidebar Sections */
    .sidebar-section {
        background: white;
        border-radius: 12px;
        padding: 1.25rem;
        margin: 1.5rem 0;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .sidebar-section-title {
        color: #64748b;
        font-weight: 700;
        font-size: 0.8rem;
        margin-bottom: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .sidebar-metric {
        background: #f8fafc;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.75rem 0;
        border: 1px solid #e2e8f0;
    }
    
    .sidebar-metric-label {
        color: #64748b;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .sidebar-metric-value {
        color: #0f172a;
        font-size: 1.5rem;
        font-weight: 800;
        margin-top: 0.25rem;
    }
    
    .sidebar-list {
        list-style: none;
        padding: 0;
        margin: 0;
    }
    
    .sidebar-list li {
        color: #475569;
        padding: 0.5rem 0;
        font-size: 0.875rem;
        display: flex;
        align-items: center;
    }
    
    .sidebar-list li:before {
        content: "•";
        color: #3b82f6;
        margin-right: 0.75rem;
        font-weight: 800;
    }
    
    /* Status Indicators - Medical Colors */
    .status-critical {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        border-left: 4px solid #dc2626;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.1);
    }
    
    .status-warning {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-left: 4px solid #f59e0b;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.1);
    }
    
    .status-success {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 4px solid #10b981;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.1);
    }
    
    .status-info {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-left: 4px solid #3b82f6;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
    }
    
    /* Metrics - Modern Cards */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #f1f5f9;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.875rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
    }
    
    .metric-delta {
        font-size: 0.875rem;
        color: #10b981;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    /* Buttons - Modern Gradient */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 1rem 2rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.35);
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 35px rgba(59, 130, 246, 0.45);
    }
    
    /* Timeline - Modern Medical Record */
    .timeline-item {
        border-left: 3px solid #e2e8f0;
        padding-left: 2rem;
        margin: 2rem 0;
        position: relative;
    }
    
    .timeline-item:before {
        content: "";
        position: absolute;
        left: -8px;
        width: 14px;
        height: 14px;
        border-radius: 50%;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        box-shadow: 0 0 0 4px white, 0 0 0 6px #e2e8f0;
    }
    
    .timeline-date {
        font-weight: 700;
        color: #0f172a;
        font-size: 1rem;
        margin-bottom: 0.25rem;
    }
    
    .timeline-event {
        color: #475569;
        font-size: 0.95rem;
        margin: 0.5rem 0;
    }
    
    .timeline-type {
        display: inline-block;
        background: #f1f5f9;
        color: #64748b;
        padding: 0.25rem 0.75rem;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    /* Tabs - Modern Style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8fafc;
        padding: 0.75rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 1rem 1.75rem;
        background: transparent;
        font-weight: 600;
        color: #64748b;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        color: #3b82f6;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Expander - Modern Accordion */
    .streamlit-expanderHeader {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        font-weight: 600;
        padding: 1rem 1.5rem;
    }
    
    .streamlit-expanderHeader:hover {
        background: #f1f5f9;
        border-color: #3b82f6;
    }
    
    /* Text Areas */
    .stTextArea textarea {
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        font-family: 'Plus Jakarta Sans', sans-serif;
        padding: 1rem;
    }
    
    .stTextArea textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.1);
    }
    
    /* Section Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 3rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = DocWeaverOrchestrator()
if 'workflow_results' not in st.session_state:
    st.session_state.workflow_results = None
if 'api_key_set' not in st.session_state:
    st.session_state.api_key_set = False


def check_api_key():
    """Check if API key is configured"""
    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "your_gemini_api_key_here":
        st.sidebar.error("⚠️ API Key Required")
        api_key_input = st.sidebar.text_input(
            "Enter Gemini API Key:",
            type="password"
        )
        if api_key_input:
            os.environ["GEMINI_API_KEY"] = api_key_input
            Config.GEMINI_API_KEY = api_key_input
            st.session_state.api_key_set = True
            st.sidebar.success("✓ Configured")
            st.rerun()
        return False
    return True


def main():
    """Main application"""
    
    # Hero Header
    st.markdown("""
    <div class="hero-header">
        <div class="hero-title">DocWeaver Clinical Intelligence</div>
        <div class="hero-subtitle">Multi-Agent AI Orchestration for Healthcare Documentation</div>
        <span class="hero-badge">Powered by Gemini 3 Flash</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Check API key
    if not check_api_key():
        st.markdown('<div class="status-info">', unsafe_allow_html=True)
        st.markdown("### 🔑 Get Started")
        st.markdown("""
        **Quick Setup:**
        1. Visit [Google AI Studio](https://aistudio.google.com/)
        2. Generate API key
        3. Enter in sidebar
        """)
        st.markdown('</div>', unsafe_allow_html=True)
        return
    
    # Modern Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-logo">Doc<span class="sidebar-logo-accent">Weaver</span></div>', unsafe_allow_html=True)
        
        page = st.radio(
            "",
            ["🏠 Home", "📊 Clinical Data Fusion", "📝 Smart Documentation", 
             "🔗 Care Coordination", "⚡ Complete Workflow", "📈 Analytics Dashboard"],
            label_visibility="collapsed"
        )
        
        # Status Section
        if st.session_state.workflow_results:
            api_count = st.session_state.workflow_results.get('summary', {}).get('total_api_calls', 0)
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-section-title">System Status</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="sidebar-metric">
                <div class="sidebar-metric-label">API Calls</div>
                <div class="sidebar-metric-value">{api_count}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        # About Section
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-section-title">Platform Features</div>', unsafe_allow_html=True)
        st.markdown("""
        <ul class="sidebar-list">
            <li>20+ AI agents</li>
            <li>Real-time processing</li>
            <li>Temporal analysis</li>
            <li>Auto-coordination</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Route to pages
    if page == "🏠 Home":
        show_home()
    elif page == "📊 Clinical Data Fusion":
        show_clinical_data_fusion()
    elif page == "📝 Smart Documentation":
        show_smart_documentation()
    elif page == "🔗 Care Coordination":
        show_care_coordination()
    elif page == "⚡ Complete Workflow":
        show_complete_workflow()
    elif page == "📈 Analytics Dashboard":
        show_analytics_dashboard()


def show_home():
    """Modern home page"""
    
    # Feature Cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Clinical Data Fusion</div>
            <div class="feature-subtitle">Multi-source medical record analysis</div>
            <ul class="feature-list">
                <li>Process documents sequentially with AI agents</li>
                <li>Detect temporal trends across time</li>
                <li>Establish causal relationships</li>
                <li>~13 specialized API calls</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📝</div>
            <div class="feature-title">Smart Documentation</div>
            <div class="feature-subtitle">AI-powered clinical note generation</div>
            <ul class="feature-list">
                <li>Transform brief notes into complete SOAP</li>
                <li>Automatic ICD-10 code extraction</li>
                <li>CPT code determination</li>
                <li>6 specialized API calls</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔗</div>
            <div class="feature-title">Care Coordination</div>
            <div class="feature-subtitle">Automated workflow orchestration</div>
            <ul class="feature-list">
                <li>Generate referral letters automatically</li>
                <li>Schedule follow-up appointments</li>
                <li>Create patient communications</li>
                <li>3+ specialized API calls</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Demo Section
    st.markdown("""
    <div class="demo-section">
        <div class="demo-title">🎬 Try Our Demo</div>
        <div class="demo-subtitle">Experience DocWeaver with Sarah Chen, a 52-year-old patient with Type 2 Diabetes</div>
        <div class="demo-list">
            <ul style="list-style: none; padding: 0; margin: 0;">
                <li>Recent ER visit for chest pain (cardiac cause ruled out)</li>
                <li>Lab analysis shows A1C increasing from 6.5% to 6.8%</li>
                <li>New microalbuminuria indicates early kidney disease</li>
                <li>AI identifies causal link: Ibuprofen + ACE inhibitor affecting kidney function</li>
                <li>System auto-generates ophthalmology referral</li>
                <li>Creates patient education materials</li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Demo Button
    if st.button("🚀 Launch Complete Demo", type="primary"):
        with st.spinner("Processing clinical workflow... 5-7 minutes"):
            demo_files = [
                "demo_data/sarah_chen_lab_6months.txt",
                "demo_data/sarah_chen_lab_recent.txt",
                "demo_data/sarah_chen_er_discharge.txt",
                "demo_data/sarah_chen_cardiology_consult.txt",
                "demo_data/sarah_chen_last_visit.txt"
            ]
            
            brief_note = "52F DM2 f/u, ER visit for CP ruled out, D/C ibuprofen due to kidney concerns, start atorvastatin 20mg for LDL 145, increase lisinopril to 40mg, A1C up to 6.8%, new microalbuminuria 35, refer ophthalmology"
            
            try:
                results = asyncio.run(
                    st.session_state.orchestrator.run_complete_workflow(demo_files, brief_note)
                )
                
                st.session_state.workflow_results = results
                st.balloons()
                st.success("✓ Workflow completed! View results in Analytics Dashboard.")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                with st.expander("Technical Details"):
                    st.code(traceback.format_exc())
    
    # Quick Results
    if st.session_state.workflow_results:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### ⚡ Quick Results")
        
        summary = st.session_state.workflow_results['summary']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">API Calls</div>
                <div class="metric-value">{summary['total_api_calls']}</div>
                <div class="metric-delta">↑ Multi-agent system</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Time</div>
                <div class="metric-value">{summary['processing_time_seconds']:.0f}s</div>
                <div class="metric-delta">↓ 45 min saved</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Documents</div>
                <div class="metric-value">{summary['documents_processed']}</div>
                <div class="metric-delta">✓ Processed</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Actions</div>
                <div class="metric-value">{summary['actions_automated']}</div>
                <div class="metric-delta">✓ Automated</div>
            </div>
            """, unsafe_allow_html=True)


def show_clinical_data_fusion():
    """Clinical Data Fusion feature (formerly Feature 2)"""
    st.markdown("## 📊 Clinical Data Fusion")
    st.markdown("Multi-source medical record analysis with temporal reasoning")
    
    st.markdown("### Document Upload")
    
    use_demo = st.checkbox("Use demo patient data (Sarah Chen)", value=True)
    
    if use_demo:
        st.markdown('<div class="status-info">📁 Using 5 medical documents for Sarah Chen (MRN: 12345678)</div>', unsafe_allow_html=True)
        demo_files = [
            "demo_data/sarah_chen_lab_6months.txt",
            "demo_data/sarah_chen_lab_recent.txt",
            "demo_data/sarah_chen_er_discharge.txt",
            "demo_data/sarah_chen_cardiology_consult.txt",
            "demo_data/sarah_chen_last_visit.txt"
        ]
        
        if st.button("Process Medical Records", type="primary"):
            with st.spinner("Analyzing medical records... 2-3 minutes"):
                try:
                    results = asyncio.run(
                        st.session_state.orchestrator.process_patient_documents(demo_files)
                    )
                    st.session_state.feature_2_results = results
                    st.success(f"✓ Processed {results['documents_count']} documents using {results['api_calls_used']} API calls")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # Display results (keeping your existing result display logic but with better styling)
    if 'feature_2_results' in st.session_state:
        results = st.session_state.feature_2_results
        
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("### 📋 Analysis Results")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Documents", results['documents_count'])
        col2.metric("API Calls", results['api_calls_used'])
        col3.metric("Timeline Events", len(results['temporal_analysis']['timeline']))
        col4.metric("Causal Links", len(results['temporal_analysis']['causal_analysis'].get('causal_links', [])))
        
        # ... rest of your Feature 2 display code ...


def show_smart_documentation():
    """Smart Documentation feature (formerly Feature 8)"""
    st.markdown("## 📝 Smart Documentation")
    st.markdown("AI-powered clinical note generation with billing codes")
    
    # ... rest of your Feature 8 code ...


def show_care_coordination():
    """Care Coordination feature (formerly Feature 9)"""
    st.markdown("## 🔗 Care Coordination")
    st.markdown("Automated workflow orchestration and patient communications")
    
    # ... rest of your Feature 9 code ...


def show_complete_workflow():
    """Complete Workflow"""
    st.markdown("## ⚡ Complete Workflow")
    st.markdown("Run all features in integrated multi-agent workflow")
    
    # ... rest of your workflow code ...


def show_analytics_dashboard():
    """Analytics Dashboard (formerly Metrics Dashboard)"""
    st.markdown("## 📈 Analytics Dashboard")
    st.markdown("Performance metrics and system insights")
    
    # ... rest of your metrics code ...


if __name__ == "__main__":
    main()