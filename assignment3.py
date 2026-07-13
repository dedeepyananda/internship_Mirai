import streamlit as st
from google import genai
import os
from dotenv import load_dotenv

st.title("The Multiverse of Chatbots 🤖")

# Sidebar
st.sidebar.title("Multiverse of Chatbots 🤖")

personality = st.sidebar.selectbox(
    "Select a personality to chat with 🦹‍♀️:",
    [
        "A Small Kid", "A Teacher", "A Doctor", "A Therapist",
        "A Comedian", "An Actor", "A Scientist",
        "A Depressed Person", "A Happy Person", "A Sad Person",
        "A Motivational Speaker", "A Politician", "A Singer",
        "A Dancer", "A Chef", "A Gamer",
        "A Programmer", "A Writer", "A Poet"
    ]
)

intensity = st.sidebar.slider(
    f"Intensity of {personality}:",
    min_value=1,
    max_value=10,
    value=1
)

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- MAIN CHAT ----------------

# Display previous messages in main page
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
if user_message := st.chat_input("Say something..."):

    # Show user message
    with st.chat_message("user"):
        st.write(user_message)

    st.session_state.messages.append(
        {"role": "user", "content": user_message}
    )

    ai_instructions = (
        f"You are acting as {personality}. "
        f"Respond completely in character. "
        f"Character intensity is {intensity}/10."
    )

    with st.spinner("Connecting to the Multiverse..."):

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{ai_instructions}\nUser: {user_message}"
        )

    # Display AI response
    with st.chat_message("assistant"):
        st.write(response.text)

    # Save AI response
    st.session_state.messages.append(
        {"role": "assistant", "content": response.text}
    )

# ---------------- SIDEBAR HISTORY ----------------
st.sidebar.markdown("---")
st.sidebar.subheader("Chat History")

titles = []

for msg in st.session_state.messages:
    if msg["role"] == "user":
        title = msg["content"][:35]
        if len(msg["content"]) > 35:
            title += "..."
        titles.append(title)

# Remove duplicates
titles = list(dict.fromkeys(titles))

for title in titles:
    st.sidebar.button(title, use_container_width=True)