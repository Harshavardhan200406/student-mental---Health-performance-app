import streamlit as st
import joblib
import pandas as pd
import time
import random

# Load the trained model
try:
    model = joblib.load('student_performance_model.pkl')
except FileNotFoundError:
    st.error("Model file not found. Please run 'train_model.py' first.")
    st.stop()

# --- 1. Chatbot Logic (Rule-Based) ---
def get_bot_response(user_input):
    user_input = user_input.lower()
    
    # Simple Keyword Matching
    if "stress" in user_input or "worried" in user_input:
        return "I understand. Exams can be stressful. Try the '5-4-3-2-1' grounding technique to calm down."
    elif "sleep" in user_input or "tired" in user_input:
        return "Sleep is crucial for memory. Try to get at least 7 hours tonight. Avoid screens 1 hour before bed."
    elif "grades" in user_input or "marks" in user_input or "fail" in user_input:
        return "Don't panic about grades. Focus on one subject at a time. Have you tried the Pomodoro technique?"
    elif "hello" in user_input or "hi" in user_input:
        return "Hello there! I am your Student Support Bot. How are you feeling today?"
    elif "sad" in user_input or "depressed" in user_input:
        return "I'm sorry you're feeling this way. Please talk to a friend or campus counselor. You are not alone. 💙"
    elif "help" in user_input or "advice" in user_input:
        return "I'm here to help! You can ask me about study habits, stress management, or sleep tips."
    elif "thank" in user_input:
        return "You're welcome! Remember, taking care of your mental health is just as important as academics."
    elif "bye" in user_input or "see you" in user_input:
        return "Goodbye! Take care of yourself and reach out if you need anything."
    elif "exercise" in user_input or "workout" in user_input:
        return "Physical activity can boost your mood and focus. Even a 10-minute walk can help clear your mind!"
    elif "time management" in user_input or "procrastination" in user_input:
        return "Time management is key! Try breaking tasks into smaller chunks and use a timer to stay on track."
    elif "social" in user_input or "friends" in user_input:
        return "Social connections are important. Try to spend time with friends or join a campus club to meet new people." 
    elif "mindfulness" in user_input or "meditation" in user_input:
        return "Mindfulness can reduce stress. Try a simple meditation: Sit quietly, focus on your breath, and let thoughts pass without judgment."
    elif "nutrition" in user_input or "food" in user_input:
        return "Eating well can improve your energy and focus. Try to include fruits, veggies, and whole grains in your diet!"
    elif "motivation" in user_input or "inspiration" in user_input:
        quotes = [
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
            "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "You are never too old to set another goal or to dream a new dream. - C.S. Lewis"
        ]
        return random.choice(quotes)
    elif "study tips" in user_input or "focus" in user_input:
        return "Here are some study tips: 1) Use active recall and spaced repetition. 2) Take regular breaks. 3) Find a quiet, comfortable study space."        
    elif "mental health" in user_input or "well-being" in user_input:
        return "Your mental health is important. Make sure to take breaks, connect with friends, and seek support if you're struggling."
    elif "campus resources" in user_input or "counseling" in user_input:
        return "Most campuses have counseling centers, support groups, and wellness programs. Check your university's website for resources available to you."
    elif "self-care" in user_input or "relaxation" in user_input:
        return "Self-care is essential. Consider activities like reading, taking a bath, listening to music, or spending time in nature to relax and recharge."
    elif "academic pressure" in user_input or "overwhelmed" in user_input:
        return "Academic pressure can be tough. Remember to set realistic goals, prioritize tasks, and don't hesitate to ask for help when needed."
    elif "confidence" in user_input or "self-esteem" in user_input:
        return "Building confidence takes time. Celebrate small victories, focus on your strengths, and remember that everyone has unique talents to offer."  
    elif "burnout" in user_input or "exhausted" in user_input:
        return "Burnout is a sign you need to take a break. Try to step away from work, engage in a hobby, or spend time with loved ones to recharge."
    elif "anxiety" in user_input or "nervous" in user_input:
        return "Anxiety can be overwhelming. Try deep breathing exercises, grounding techniques, or talking to someone you trust about how you're feeling."
    else:
        return "I'm listening. Tell me more about your study habits or daily routine."

# --- 2. Main App UI ---
def main():
    st.set_page_config(page_title="Student Mental Health System", layout="wide")
    
    # Sidebar for Navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.radio("Go to", ["Prediction System", "Counselor Chatbot"])

    # --- PAGE 1: Prediction System ---
    if app_mode == "Prediction System":
        st.title("Student Performance Prediction")
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Academic Data")
            study_hours = st.slider("Daily Study Hours", 0, 15, 4)
            attendance = st.slider("Attendance (%)", 0, 100, 75)
            marks = st.number_input("Average Marks", 0, 100, 60)
            backlogs = st.number_input("Number of Backlogs", 0, 10, 0)

        with col2:
            st.subheader("Behavioral Data")
            sleep_hours = st.slider("Daily Sleep Hours", 0, 12, 7)
            screen_time = st.slider("Daily Screen Time (Hrs)", 0, 15, 5)

        if st.button("Predict Performance"):
            input_data = pd.DataFrame([[study_hours, attendance, marks, backlogs, sleep_hours, screen_time]],
                                      columns=['StudyHours', 'Attendance', 'Marks', 'Backlogs', 'SleepHours', 'ScreenTime'])
            
            with st.spinner('Analyzing...'):
                time.sleep(1) 
                prediction = model.predict(input_data)[0]

            st.divider()
            st.subheader(f"Predicted Performance: {prediction}")
            
            if prediction == 'Excellent':
                st.success("Great job! Keep maintaining this balance.")
            elif prediction == 'Good':
                st.info("Good work! A little more focus on weak areas will help.")
            elif prediction == 'Average':
                st.warning("Warning: Focus on attendance and reducing screen time.")
            else:
                st.error("Alert: Please reach out to a mentor. Prioritize sleep and mental health.")

    # --- PAGE 2: Counselor Chatbot ---
    elif app_mode == "Counselor Chatbot":
        st.title("Student Counselor")
        st.write("Chat with me about stress, sleep, or study tips!")

        # Initialize chat history in session state
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat Input Field
        if prompt := st.chat_input("Type here... (e.g., 'I feel stressed')"):
            
            # 1. Show User Message
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})

            # 2. Generate Bot Response
            response = get_bot_response(prompt)

            # 3. Show Bot Message
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == '__main__':
    main()
