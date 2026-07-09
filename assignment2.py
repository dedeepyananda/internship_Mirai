import streamlit as st 
from google import genai
import os
from dotenv import load_dotenv
st.title("The Multiverse of Chatbots 🤖")
personality=st.selectbox("Select a personality to chat with 👱:",
                         ["A Small Kid","A Teacher","A Doctor","A Therapist","A Comedian","An Actor","A Scientist","A Depressed Person","A Happy Person","A Sad Person","A Motivational Speaker","A Politician","A Singer","A Dancer","A Chef","A Gamer","A Programmer","A Writer","A Poet"])
load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
user_message=st.text_input("say some thing?")
if st.button("send"):
    if user_message:
        ai_instructions=f"you are acting as {personality} and you are responding to the user staying completly in character"
        with st.spinner("connecting to multiverse...."):
            response=client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{ai_instructions}\nUser: {user_message}\n{personality}:"
            )
            st.success("response received")
            st.write(response.text)
    else:
        st.warning("please enter a message to send to the chatbot")
