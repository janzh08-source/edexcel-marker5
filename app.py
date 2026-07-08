import streamlit as st
import google.generativeai as genai

# Set up the Gemini API
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("Edexcel AI Marker")
subject = st.selectbox("Select Subject", ["Maths", "English"])
student_answer = st.text_area("Paste your answer here:")

if st.button("Grade My Work"):
    if student_answer:
        prompt = f"You are an expert Edexcel examiner. Grade this {subject} response: {student_answer}"
        response = model.generate_content(prompt)
        st.write(response.text)
