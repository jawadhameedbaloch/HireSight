# HireSight - Be Seen, Be Hired 

**HireSight** is an advanced AI-powered resume screening and matching application designed to streamline the recruitment process. It leverages Natural Language Processing (NLP) and Machine Learning (ML) to analyze resumes against job descriptions (JDs), providing a semantic match score that goes beyond simple keyword matching.

## Live site
https://hiresight.streamlit.app 

##  Features

###  Resume & Job Description Analysis
- **Dual Input Support:** Upload Resumes and Job Descriptions in **PDF format** or paste text directly.
- **Automated Text Extraction:** Seamlessly extracts text from PDF documents.

###  Intelligent Skill Extraction
- **Keyword Matching:** Identifies key technical skills (e.g., Python, React, AWS) from both documents.
- **Gap Analysis:** Highlights **Matching Skills** and **Missing Skills** to give clear feedback.

###  Semantic Matching Engine
- **Advanced NLP:** Uses `sentence-transformers` (Model: `all-MiniLM-L6-v2`) to generate vector embeddings.
- **Cosine Similarity:** Calculates a precise **Match Score (0-100%)** based on semantic meaning, not just keywords.
- **Suitability Assessment:** Automatically flags candidates as "Suitable" based on a configurable threshold.

###  Modern UI
- **Dark Mode Aesthetic:** Sleek, professional interface with glassmorphism effects.
- **Interactive Results:** Visual metrics and clear success/error indicators.

##  Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/)
- **Language:** Python 3.x
- **ML & NLP:** `sentence-transformers`, `scikit-learn`, `torch`
- **Data Processing:** `pandas`, `PyMuPDF (fitz)`

##  Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/jawadhameedbaloch/HireSight.git
   cd HireSight
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

##  Usage

1. **Run the application:**
   ```bash
   streamlit run app/app.py
   ```

2. **Open your browser:**
   The app will typically open at `http://localhost:8501`.

3. **Start Matching:**
   - Click "Start Now".
   - Upload a Resume (PDF) and a Job Description (PDF).
   - Click "Analyze Match" to see the score and skill breakdown.

##  Model Analysis

The project includes a comprehensive analysis pipeline (`notebook/HireSight_full.ipynb`) used for model testing and performance evaluation.



##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

##  License

This project is open source.
