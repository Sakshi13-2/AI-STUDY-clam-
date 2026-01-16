import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="AI Study Calm", layout="centered")

st.title("🧘 AI Study Calm")
st.write("When the syllabus feels like a mountain, let's turn it into a few steps.")

# User Input Section
with st.container():
    subj = st.text_input("What are you preparing for?", placeholder="e.g. Final Math Exam")
    c1, c2 = st.columns(2)
    with c1:
        chaps = st.number_input("How many topics/chapters are left?", min_value=1, value=5)
    with c2:
        days = st.number_input("How many days do you have?", min_value=1, value=2)
    
    mood = st.select_slider("How stressed do you feel right now?", options=list(range(1, 11)), value=7)

if st.button("Help me feel prepared"):
    payload = {"subject": subj, "total_chapters": chaps, "days_left": days, "current_mood": mood}
    
    try:
        res = requests.post("http://127.0.0.1:8000/generate_plan", json=payload).json()
        
        st.divider()
        st.subheader(f"✨ Exam Readiness Score: {res['readiness_score']}")
        st.info(f"💡 **AI Message:** {res['message']}")
        
        # Micro-Goal Logic
        st.write(f"### 🎯 Your Micro-Plan for today")
        st.write(f"Instead of {chaps} chapters, you only need to finish **{res['tasks_per_day']} small steps** today.")
        
        for goal in res['micro_goals']:
            st.checkbox(goal)
            
        # Anxiety Reduction Visualization
        st.write("---")
        st.write("### 📉 Anxiety Reduction Projection")
        st.write("Completing these tiny tasks will lower your stress by shifting your focus from 'The Exam' to 'The Step'.")
        
        # Chart: Mastery goes UP, Anxiety goes DOWN
        data = pd.DataFrame({
            'Progress Step': ['Start', 'Goal 1', 'Goal 2', 'Goal 3'],
            'Confidence': [20, 45, 70, 95],
            'Anxiety': [mood*10, mood*7, mood*4, 10]
        }).set_index('Progress Step')
        st.line_chart(data)
        
    except:
        st.error("Error: Did you run 'python backend.py' in your terminal?")