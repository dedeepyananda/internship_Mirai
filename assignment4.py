import streamlit as st
import random
import requests
from urllib.parse import quote
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
env_var = os.getenv("GEMINI_API_KEY")
print(env_var)

# Page Title
st.set_page_config(page_title="AI Image Studio", page_icon="🎨")

st.title("🎨 The AI Image Studio")
st.sidebar.title("Generation Settings")

# Sidebar Settings
art_style = st.sidebar.selectbox(
    "Select a style for the image:",
    [
        "Realistic",
        "Cartoon",
        "Abstract",
        "Fantasy",
        "Sci-Fi",
        "Aesthetic",
        "Minimalist",
        "Surreal",
        "Pop Art",
        "Impressionist"
    ]
)

width = st.sidebar.slider(
    "Width",
    min_value=256,
    max_value=1024,
    value=512,
    step=64
)

height = st.sidebar.slider(
    "Height",
    min_value=256,
    max_value=1024,
    value=512,
    step=64
)

magic_enhance = st.sidebar.checkbox("✨ Enable Magic Enhance")

# Surprise Prompts
surprise_prompts = [
    "An astronaut riding a horse on Mars",
    "A cyberpunk street food vendor in Tokyo",
    "A giant panda working as a chef",
    "A floating castle above the clouds",
    "A dragon playing cricket in a stadium"
]

# Initialize session state
if "prompt" not in st.session_state:
    st.session_state["prompt"] = ""

# Surprise Me Button
if st.button("🎲 Surprise Me!"):
    st.session_state["prompt"] = random.choice(surprise_prompts)

# Prompt Input
user_prompt = st.text_input(
    "Enter your prompt for the image:",
    key="prompt"
)

# Generate Button
if st.button("Generate Image"):
    if user_prompt.strip():

        full_prompt = f"{user_prompt}, {art_style} style"

        # Magic Enhance
        if magic_enhance:
            full_prompt += (
                ", masterpiece, 8k resolution, highly detailed, "
                "cinematic lighting, sharp focus, trending on ArtStation, "
                "Unreal Engine 5 render"
            )

        # Encode URL
        url = (
            f"https://image.pollinations.ai/prompt/"
            f"{quote(full_prompt)}?width={width}&height={height}"
        )

        with st.spinner("🎨 Rendering image..."):
            response = requests.get(url)

        if response.status_code == 200:
            st.success("✅ Image Generated Successfully!")

            st.image(
                response.content,
                caption=full_prompt,
                use_container_width=True
            )

            st.download_button(
                label="📥 Download Image",
                data=response.content,
                file_name="my_ai_image.png",
                mime="image/png"
            )

        else:
            st.error(
                f"❌ Failed to generate image. Status Code: {response.status_code}"
            )

    else:
        st.warning("⚠️ Please enter a prompt before generating the image.")