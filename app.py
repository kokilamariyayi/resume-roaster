import streamlit as st
from roaster import roast_resume
import pdfplumber
import io
import os
import json
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# --- Configuration & Styling ---
st.set_page_config(page_title="Beat-The-ATS", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

# Inject custom CSS for a premium look
st.markdown("""
    <style>
    :root {
        --primary: #6366f1;
        --secondary: #a855f7;
        --background: #0f172a;
        --surface: #1e293b;
        --text: #f8fafc;
        --text-muted: #94a3b8;
    }
    .stApp {
        background-color: var(--background);
        color: var(--text);
    }
    /* Premium Button */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(99, 102, 241, 0.4), 0 4px 6px -2px rgba(99, 102, 241, 0.2);
    }
    /* Card Styling */
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border-left: 4px solid var(--primary);
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateX(5px);
    }
    .metric-title {
        font-size: 0.9rem;
        color: var(--text-muted);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: white;
    }
    .metric-date {
        font-size: 0.8rem;
        color: var(--text-muted);
        margin-top: 0.5rem;
    }
    /* Headers & Dividers */
    h1, h2, h3 { color: white; font-weight: 700; }
    hr { border-color: rgba(255,255,255,0.1); }
    /* Inputs */
    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: var(--surface) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 1px var(--primary) !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- History Helper ---
HISTORY_FILE = "history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(role, score, mode):
    history = load_history()
    history.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "role": role,
        "score": score,
        "mode": mode
    })
    # Keep only last 5 entries
    with open(HISTORY_FILE, "w") as f:
        json.dump(history[-5:], f)

# --- Header ---
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>🚀 Beat-The-ATS</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.2rem; margin-bottom: 2rem;'>Multi-level Analysis • Role Inference • Career Optimization</p>", unsafe_allow_html=True)

# Load API key
api_key = os.getenv("GROQ_API_KEY", "")

# --- Sidebar: History & Insights ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=60) # Placeholder icon
    st.header("📈 Career Progress")
    history = load_history()
    if history:
        for entry in reversed(history):
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-title">{entry['role']}</div>
                <div class="metric-value">Score: {entry['score']}</div>
                <div class="metric-date">🕒 {entry['date']} • {entry['mode'].replace('_', ' ')}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No history found. Start your first analysis!")
        
    st.markdown("---")
    st.caption("Powered by Groq & Llama 3.3")

# --- Main Interface ---
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📄 Candidate Profile")
    
    # Target Role Dropdown + Custom
    common_roles = [
        "Software Engineer", "Data Scientist", "Machine Learning Engineer",
        "Product Manager", "Data Analyst", "Backend Developer", 
        "Frontend Developer", "Full Stack Developer", "DevOps Engineer",
        "Other (Type below)"
    ]
    selected_role = st.selectbox("🎯 Target Role", common_roles)
    
    if selected_role == "Other (Type below)":
        target_role = st.text_input("Specify Target Role", placeholder="e.g. Quantitative Analyst")
    else:
        target_role = selected_role
    
    # Resume Input
    input_method = st.radio("Resume Format", ["Paste Text", "Upload PDF"], horizontal=True)
    resume_text = ""
    
    if input_method == "Paste Text":
        resume_text = st.text_area("Resume Content", height=250, placeholder="Paste your full resume text here...")
    else:
        uploaded_resume = st.file_uploader("Upload Resume PDF", type=["pdf"])
        if uploaded_resume:
            with pdfplumber.open(io.BytesIO(uploaded_resume.read())) as pdf:
                resume_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            st.success("✅ Resume Extracted Successfully!")

with col2:
    st.markdown("### ⚙️ Analysis Parameters")
    
    mode = st.radio("Analysis Mode", ["WITHOUT_JD", "WITH_JD"], 
                    format_func=lambda x: "🏢 Industry Benchmark (No JD)" if x == "WITHOUT_JD" else "🎯 Job Description Alignment", 
                    horizontal=True)
    
    job_description = ""
    if mode == "WITH_JD":
        jd_input_method = st.radio("JD Format", ["Paste Text", "Upload PDF"], horizontal=True)
        if jd_input_method == "Paste Text":
            job_description = st.text_area("Job Description", height=250, placeholder="Paste the target job description here...")
        else:
            uploaded_jd = st.file_uploader("Upload JD PDF", type=["pdf"])
            if uploaded_jd:
                with pdfplumber.open(io.BytesIO(uploaded_jd.read())) as pdf:
                    job_description = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
                st.success("✅ JD Extracted Successfully!")
    else:
        st.info("ℹ️ **Benchmark Mode:** The AI will evaluate your resume against top-tier industry standards for your selected target role.")

st.markdown("<br>", unsafe_allow_html=True)

# --- Execution ---
_, center_col, _ = st.columns([1, 2, 1])
with center_col:
    analyze_btn = st.button("🚀 GENERATE INTELLIGENCE REPORT", use_container_width=True)

if analyze_btn:
    if not api_key:
        st.error("⚠️ API Key missing. Please set GROQ_API_KEY in your .env file.")
    elif not resume_text.strip():
        st.error("⚠️ Please provide a resume.")
    elif not target_role.strip():
        st.error("⚠️ Please specify a target role.")
    elif mode == "WITH_JD" and not job_description.strip():
        st.error("⚠️ Please provide a job description for Alignment Mode.")
    else:
        with st.spinner("🧠 Initializing Advanced Neural Analysis..."):
            try:
                history_data = load_history()
                history_json = json.dumps(history_data) if history_data else "None"
                
                result = roast_resume(resume_text, target_role, mode, api_key, job_description, history_json)
                
                # Extract score for history
                score = "N/A"
                for line in result.split("\n"):
                    if "ATS Score:" in line:
                        score = line.split(":")[-1].strip()
                        break
                
                save_history(target_role, score, mode)
                
                st.success("✨ Analysis Complete!")
                st.markdown("---")
                
                # Display Results in a nice container
                with st.container():
                    st.markdown("## 📊 Career Optimization Intelligence Report")
                    st.markdown(result)
                
                st.markdown("---")
                st.download_button(
                    label="⬇️ Download Full Report (.txt)",
                    data=result,
                    file_name=f"career_intel_{target_role.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"❌ Error during analysis: {e}")
