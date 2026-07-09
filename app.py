import streamlit as st
import google.generativeai as genai
import time

# Set up the Gemini API
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

st.title("Exam Board AI Marker")

# Define the hierarchy of boards and subjects
board_subjects = {
    "Edexcel": ["Maths", "Further Maths", "Physics", "Biology", "Chemistry", "Psychology", "Economics"],
    "AQA": ["Maths", "Further Maths", "Physics", "Biology", "Chemistry", "Psychology", "Economics"],
    "OCR": ["Maths", "Further Maths", "Physics", "Biology", "Chemistry", "Psychology", "Economics"],
    "WJEC": ["Maths", "Further Maths", "Physics", "Biology", "Chemistry", "Psychology", "Economics"]
}

# First level: Select the board
selected_board = st.selectbox("Select Exam Board", list(board_subjects.keys()))

# Second level: Select the subject based on the chosen board
selected_subject = st.selectbox("Select Subject", board_subjects[selected_board])

student_answer = st.text_area("Paste your answer/working out here:")

if st.button("Grade My Work"):
    if student_answer:
        with st.spinner('Analyzing your work...'):
            prompt = f"You are an expert {selected_board} examiner. Grade the following {selected_subject} answer. Provide feedback on correctness, highlight any errors, and suggest improvements based on {selected_board} criteria. Answer: {student_answer}"
            
            try:
                time.sleep(1) 
                response = model.generate_content(prompt)
                st.write("### Feedback:")
                st.write(response.text)
            except Exception as e:
                if "429" in str(e):
                    st.warning("The AI is busy! Please wait 10 seconds and try again.")
                else:
                    st.error(f"An error occurred: {e}")
    else:
        st.warning("Please paste your answer before clicking Grade.")
