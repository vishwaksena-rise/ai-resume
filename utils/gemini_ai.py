from google import genai
from dotenv import load_dotenv
import streamlit as st
import os
import httpx
import time

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Read API Key
# -----------------------------
api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found.")

# -----------------------------
# Create Gemini Client
# -----------------------------
client = genai.Client(api_key=api_key)


# -----------------------------
# Resume Analyzer
# -----------------------------
def analyze_resume(resume_text, job_role):

    prompt = f"""
You are an expert ATS Resume Analyzer.

Analyze the following resume for the role of **{job_role}**.

Give the response in the following format:

1. ATS Score (out of 100)

2. Resume Summary

3. Strengths

4. Weaknesses

5. Missing Skills

6. Suggestions for Improvement

7. Final Verdict

Resume:

{resume_text}
"""

    # Retry up to 3 times if connection fails
    for attempt in range(3):

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            return response.text

        except httpx.RemoteProtocolError:

            if attempt < 2:
                time.sleep(2)
            else:
                return (
                    "❌ Gemini server disconnected while processing your request.\n\n"
                    "Please click **Analyze Resume** again after a few seconds."
                )

        except Exception as e:

            return f"❌ Error: {str(e)}"