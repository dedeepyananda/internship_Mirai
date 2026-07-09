"""
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()
env_var = os.getenv("GEMINI_API_KEY")
print(env_var)
"""
import streamlit as st
st.title("the multiverse of chatbots")
personality=st.selectbox("who do you want to talk to?",
                         ["Virat kohli","An angry ravi shastri","A calm sachin tendulkar","A funny rohit sharma ","A serious rahul dravid"])
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client=genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
user_message=st.text_input("say some thing?")
if st.button("send"):
    if user_message:
        ai_instructions=f"you are acting as {personality} and you are responding to the user staying completly in character"
        with st.spinner("connecting to multiverse...."):
            response=client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_message
            )
            st.success("response received")
            st.write(response.text)
    else:
        st.warning("please enter a message to send to the chatbot")
