import streamlit as st
from utils.pdf_reader import extract_text_from_pdf
from utils.gemini_ai import analyze_resume

# -------------------------------
# Page Configuration
# -------------------------------
st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="centered"
)

# -------------------------------
# Load CSS
# -------------------------------
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# -------------------------------
# Header
# -------------------------------
st.title("🤖 AI Resume Analyzer")

st.markdown(
    "### Professional ATS Resume Checker\n"
    "Upload your resume and get AI-powered feedback."
)

st.divider()

# -------------------------------
# Upload Resume
# -------------------------------
uploaded_resume = st.file_uploader(
    "📄 Upload Resume (PDF / DOCX / DOC)",
    type=["pdf", "docx", "doc"],
    help="Supported formats: PDF, DOCX and DOC"
)

# -------------------------------
# Job Role
# -------------------------------
job_role = st.selectbox(
    "💼 Select Target Role",
    (
        "Software Engineer",
        "AI Engineer",
        "Machine Learning Engineer",
        "Data Scientist",
        "Embedded Engineer",
        "Electronics Engineer"
    )
)

st.divider()

# -------------------------------
# Analyze Button
# -------------------------------
analyze = st.button(
    "🚀 Analyze Resume",
    use_container_width=True
)

# -------------------------------
# Analyze Action
# -------------------------------
if analyze:

    if uploaded_resume is None:
        st.error("❌ Please upload your resume first.")

    else:

        with st.spinner("🤖 AI is analyzing your resume... Please wait..."):

            try:

                # Extract text
                resume_text = extract_text_from_pdf(uploaded_resume)

                if not resume_text.strip():
                    st.error("❌ Unable to extract text from the uploaded document.")
                    st.stop()

                # Gemini Analysis
                result = analyze_resume(
                    resume_text,
                    job_role
                )

                st.success("✅ Analysis Completed!")

                st.markdown("## 📊 AI Analysis")

                st.write(result)

            except Exception as e:

                st.error(f"❌ {e}")