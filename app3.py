import streamlit as st
import random
import requests
from google import genai
import os
from dotenv import load_dotenv
load_dotenv()
env_var = os.getenv("GEMINI_API_KEY")
print(env_var)
st.title("The AI Image Studio 🎨")
st.sidebar.title("Generation Settings")
art_style = st.sidebar.selectbox("Select a style for the image:", 
             ["Realistic", "Cartoon", "Abstract", "Fantasy", "Sci-Fi",
              "Aesthetic", "Minimalist", "Surreal", "Pop Art", "Impressionist"])

width = st.sidebar.slider("width:", min_value=256, max_value=1024, value=512, step=64)
height = st.sidebar.slider("height:", min_value=256, max_value=1024, value=512, step=64)




user_prompt = st.text_input("Enter your prompt for the image:")
if st.button("Generate Image"):
    if user_prompt:
        with st.spinner("Rendering image..."):
            full_prompt = f"{user_prompt}, make it the art style: {art_style}"
            url =f"https://image.pollinations.ai/prompt/{full_prompt}?width={width}&height={height}"
            response = requests.get(url)
            if response.status_code == 200:
                st.success("Image Generated")
                st.image(response.content, caption=full_prompt)
                st.write("Here is your generated image:")
                st.download_button(
                    label="Download Image",
                    data=response.content,
                    file_name="my_ai_image.png",
                    mime="image/*"                         #multi purpose internet mail extensions
                )
            else:
                st.error(f"Failed to generate image. Status code: {response.status_code}")
    else:
        st.warning("Please enter a prompt to generate an image.")