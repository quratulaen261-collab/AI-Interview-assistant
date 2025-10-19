import streamlit as st
import pandas as pd
import random
from gtts import gTTS
import os

st.title("AI Interview Assistant")
st.write("No API needed! This bot will ask random interview questions and give simple feedback automatically.")

# --- Question bank ---
hr_questions = [
    "Tell me about yourself.",
    "Why do you want to work with our company?",
    "What are your strengths and weaknesses?",
    "Where do you see yourself in 5 years?",
    "How do you handle stress and pressure?"
]

tech_questions = [
    "What is Python used for?",
    "Explain the difference between a list and a tuple.",
    "What is a function in programming?",
    "What is machine learning?",
    "Explain the concept of an API."
]

feedback_list = [
    "Good answer! You seem confident and clear.",
    "Nice effort, but you can give more detailed examples.",
    "Great explanation! Keep it up!",
    "Try to be more specific in your answer.",
    "Excellent! That shows good understanding."
]

# --- Functions ---
def generate_question(interview_type):
    if interview_type == "HR":
        return random.choice(hr_questions)
    else:
        return random.choice(tech_questions)

def evaluate_answer(answer):
    return random.choice(feedback_list) + f" (Score: {random.randint(6,10)}/10)"

def save_to_csv(question, answer, feedback):
    df = pd.DataFrame([[question, answer, feedback]], columns=["Question", "Answer", "Feedback"])
    if os.path.exists("interview_data.csv"):
        df.to_csv("interview_data.csv", mode='a', header=False, index=False)
    else:
        df.to_csv("interview_data.csv", index=False)

def speak(text):
    tts = gTTS(text)
    tts.save("feedback.mp3")
    os.system("start feedback.mp3")

# --- Streamlit Flow ---
interview_type = st.selectbox("Choose interview type:", ["HR", "Technical"])

if st.button("Start Interview"):
    question = generate_question(interview_type)
    st.session_state["question"] = question
    st.write("### Question:")
    st.write(question)

if "question" in st.session_state:
    answer = st.text_area("Your Answer:")
    if st.button("Submit Answer"):
        if answer.strip():
            feedback = evaluate_answer(answer)
            st.subheader("Feedback:")
            st.write(feedback)
            speak(feedback)
            save_to_csv(st.session_state["question"], answer, feedback)
            st.success("Response saved successfully!")
        else:
            st.warning("Please write an answer before submitting.")

st.markdown("---")
if st.button("Show Interview Report"):
    if os.path.exists("interview_data.csv") and os.path.getsize("interview_data.csv") > 0:
        df = pd.read_csv("interview_data.csv")
        st.dataframe(df)
    else:
        st.warning("No interview data found yet. Please answer some questions first.")
