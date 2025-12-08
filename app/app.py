import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import re
import os
import base64

# ------------------------------------------------------------------------------
# Configuration & Styling
# ------------------------------------------------------------------------------
st.set_page_config(page_title="HireSight", page_icon="👁️", layout="wide")

# Fix for potential threading/tokenizer issues
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Initialize Session State for Page Navigation
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

def start_app():
    st.session_state.page = 'app'

# Function to set background image
def set_bg_image(image_file):
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpg;base64,{b64_encoded});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)

# Apply Background if exists
if os.path.exists("bg.jpg"):
    set_bg_image("bg.jpg")

# Custom CSS for Styling
st.markdown("""
    <style>
    /* Hide Streamlit Header, Footer, and Hamburger Menu */
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Remove default top padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        font-family: 'Inter', 'Helvetica Neue', sans-serif;
        color: #ffffff;
    }

    /* Landing Page Styling */
    .landing-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        margin-top: 10vh; /* Push down from top */
        margin-bottom: 1rem;
    }
    
    .hero-title {
        font-size: 5rem;
        font-weight: 900;
        letter-spacing: -2px;
        margin-bottom: 0.5rem;
        line-height: 1.1;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }
    
    .hero-white { color: #ffffff; }
    .hero-blue { color: #3B82F6; } /* Bright Blue */

    .hero-subtitle {
        font-size: 1.5rem;
        color: #E5E7EB; /* Gray-200 for better visibility on bg */
        font-weight: 400;
        margin-bottom: 2rem;
        text-shadow: 0 1px 5px rgba(0,0,0,0.5);
    }

    /* Button Styling - Centered & Premium */
    /* Target the container of the button to center it */
    div.stButton {
        display: flex;
        justify-content: center;
    }
    
    div.stButton > button {
        background: linear-gradient(90deg, #2563EB 0%, #3B82F6 100%);
        color: white;
        border: none;
        padding: 16px 48px;
        font-size: 1.2rem;
        font-weight: 600;
        border-radius: 50px; /* Rounded pill shape */
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.39);
    }
    
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.23);
        color: white;
    }
    
    div.stButton > button:active {
        color: white;
        background: #2563EB;
    }

    /* Input Fields (Dark Mode Transparency) */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea {
        background-color: rgba(17, 24, 39, 0.8); /* Semi-transparent */
        color: white;
        border: 1px solid #374151;
        border-radius: 10px;
    }
    
    .stFileUploader > div > div > button {
        background-color: rgba(31, 41, 55, 0.8);
        color: white;
        border: 1px solid #374151;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #3B82F6 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Model & Data
# ------------------------------------------------------------------------------
@st.cache_resource
def load_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer('all-MiniLM-L6-v2')

SKILLS_DB = [
    "python", "java", "c++", "c#", "javascript", "typescript", "html", "css", "sql", "no-sql",
    "r", "swift", "kotlin", "go", "rust", "php", "ruby", "scala", "matlab",
    "react", "angular", "vue", "node.js", "django", "flask", "fastapi", "spring boot",
    "tensorflow", "pytorch", "keras", "scikit-learn", "pandas", "numpy", "opencv", "spark",
    "docker", "kubernetes", "aws", "azure", "gcp", "git", "jenkins", "jira", "tableau", "power bi",
    "excel", "linux", "unix", "hadoop", "kafka", "redis", "mongodb", "postgresql", "mysql",
    "machine learning", "deep learning", "nlp", "computer vision", "data analysis", "data science",
    "big data", "cloud computing", "devops", "agile", "scrum", "rest api", "graphql",
    "cybersecurity", "blockchain", "iot", "project management", "communication", "leadership",
    "problem solving", "teamwork", "time management"
]

# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------
def clean_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip().lower()

def extract_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_skills(text):
    text_clean = clean_text(text)
    found_skills = set()
    for skill in SKILLS_DB:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_clean):
            found_skills.add(skill)
    return list(found_skills)

def analyze_match(resume_text, jd_text):
    from sentence_transformers import util
    model = load_model()
    
    emb_resume = model.encode(resume_text, convert_to_tensor=True)
    emb_jd = model.encode(jd_text, convert_to_tensor=True)
    similarity = util.cos_sim(emb_resume, emb_jd).item()
    match_score = round(similarity * 100, 2)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    
    matched = [s for s in jd_skills if s in resume_skills]
    missing = [s for s in jd_skills if s not in resume_skills]
    
    suitability = "Yes" if match_score >= 60 else "No"
    
    return match_score, matched, missing, suitability, resume_skills, jd_skills

# ------------------------------------------------------------------------------
# Main UI
# ------------------------------------------------------------------------------
def main():
    # Logo (Top Left)
    col_logo, col_rest = st.columns([1, 5])
    with col_logo:
        if os.path.exists("dark.png"):
            st.image("dark.png", width=180)
        else:
            st.markdown("### HireSight")

    if st.session_state.page == 'landing':
        # Hero Section
        st.markdown("""
            <div class="landing-container">
                <div class="hero-title">
                    <span class="hero-white">BE SEEN</span> <span class="hero-blue">BE HIRED</span>
                </div>
                <div class="hero-subtitle">
                    Elevate Your Resume. Bypass Every ATS Scan.
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Start Button (Centered using narrow middle column and flexbox)
        c1, c2, c3 = st.columns([5, 2, 5])
        with c2:
            st.button("Start Now →", on_click=start_app)

    elif st.session_state.page == 'app':
        # Application View
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Upload Resume")
            resume_file = st.file_uploader("PDF Format", type=["pdf"], key="resume")
            resume_txt = st.text_area("Or paste text", height=150, key="resume_txt")
            
        with col2:
            st.subheader("Job Description")
            jd_file = st.file_uploader("PDF Format", type=["pdf"], key="jd")
            jd_txt = st.text_area("Or paste text", height=150, key="jd_txt")
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Center Analyze Button
        c1, c2, c3 = st.columns([5, 2, 5])
        with c2:
            analyze_btn = st.button("Analyze Match")

        if analyze_btn:
            final_resume = ""
            if resume_file: final_resume = extract_pdf(resume_file)
            elif resume_txt: final_resume = resume_txt
            
            final_jd = ""
            if jd_file: final_jd = extract_pdf(jd_file)
            elif jd_txt: final_jd = jd_txt
            
            if not final_resume or not final_jd:
                st.error("Please provide both Resume and Job Description.")
            else:
                with st.spinner("Analyzing..."):
                    score, matched, missing, suitable, r_skills, j_skills = analyze_match(final_resume, final_jd)
                
                st.markdown("---")
                
                # Results
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Match Score", f"{score}%")
                with m2:
                    st.metric("Matched Skills", len(matched))
                with m3:
                    st.metric("Suitability", suitable)
                
                st.markdown("---")
                
                r1, r2 = st.columns(2)
                with r1:
                    st.subheader("Matching Skills")
                    if matched:
                        st.success(", ".join([s.title() for s in matched]))
                    else:
                        st.warning("None")
                with r2:
                    st.subheader("Missing Skills")
                    if missing:
                        st.error(", ".join([s.title() for s in missing]))
                    else:
                        st.info("None")

if __name__ == "__main__":
    main()
