import streamlit as st
from roaster import roast_resume
import pdfplumber
import io

st.set_page_config(page_title="Resume Roaster 🔥", page_icon="🔥", layout="centered")

st.title("🔥 Resume Roaster")
st.markdown("Paste your resume or upload a PDF — get **brutally honest AI feedback** so recruiters don't ghost you.")
st.divider()

# Groq API key input
api_key = st.text_input("🔑 Enter your Groq API Key", type="password", help="Get a free key at console.groq.com")

st.subheader("📄 Your Resume")
input_method = st.radio("Input Method", ["Paste Text", "Upload PDF"], horizontal=True)

resume_text = ""

if input_method == "Paste Text":
    resume_text = st.text_area("Paste resume content here", height=300, placeholder="Paste your resume text...")

elif input_method == "Upload PDF":
    uploaded = st.file_uploader("Upload Resume PDF", type=["pdf"])
    if uploaded:
        with pdfplumber.open(io.BytesIO(uploaded.read())) as pdf:
            resume_text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        st.success("PDF extracted successfully!")
        with st.expander("Preview Extracted Text"):
            st.text(resume_text[:1000] + "..." if len(resume_text) > 1000 else resume_text)

st.divider()

if st.button("🔥 Roast My Resume", use_container_width=True, type="primary"):
    if not api_key:
        st.error("Please enter your Groq API key.")
    elif not resume_text.strip():
        st.error("Please provide your resume content.")
    else:
        with st.spinner("Roasting your resume... 🔥"):
            try:
                result = roast_resume(resume_text, api_key)
                st.divider()
                st.subheader("🧨 Here's Your Roast")
                st.markdown(result)

                st.divider()
                st.download_button(
                    label="⬇️ Download Feedback as .txt",
                    data=result,
                    file_name="resume_roast_feedback.txt",
                    mime="text/plain",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error: {e}")

st.divider()
st.caption("Built by [Kokila M](https://github.com/kokilamariyayi) | Powered by Groq + Llama 3")
