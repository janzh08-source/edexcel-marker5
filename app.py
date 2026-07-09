import streamlit as st
import google.generativeai as genai
import time

# Set up the Gemini API
# Ensure you have saved GOOGLE_API_KEY in your Streamlit Secrets settings
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# Using the stable, frontier-class model
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("Edexcel AI Marker")

# UI for the student
subject = st.selectbox("Select Subject", ["Maths", "English"])
student_answer = st.text_area("Paste your answer/working out here:")

# Button to trigger the AI marking
if st.button("Grade My Work"):
    if student_answer:
        with st.spinner('Analyzing your work...'):
            prompt = f"You are an expert Edexcel examiner. Grade the following {subject} answer. Provide feedback on correctness, highlight any errors, and suggest improvements. Answer: {student_answer}"
            
            try:
                # Add a small delay to help stay within rate limits
                time.sleep(1) 
                response = model.generate_content(prompt)
                st.write("### Feedback:")
                st.write(response.text)
            except Exception as e:
                # Basic handling for rate limits
                if "429" in str(e):
                    st.warning("The AI is a bit busy. Please wait 10 seconds and try again.")
                else:
                    st.error(f"An error occurred: {e}")
    else:
        st.warning("Please paste your answer before clicking Grade.")
