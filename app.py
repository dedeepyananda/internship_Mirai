import streamlit as st
import requests
import json
import os

from urllib.parse import quote
from dotenv import load_dotenv
from google import genai
from gtts import gTTS

load_dotenv()
@st.cache_resource
def load_client():
    return genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
client = load_client()

st.set_page_config(
    page_title="AI visual novel",
    page_icon="📖"
)
st.title("📖 AI Multi-Modal Visual Novel")

#sidebar

st.sidebar.title("📖 Story Settings")
genre=st.sidebar.selectbox(
    "Genre",
    ["Fantasy","Horror","sci-fi","Adventurer"]
)
art_style= st.sidebar.selectbox("Art Style",
                           ["Anime","Realstic","Pixel Art","Watercolor","Oil Painting"]
                           )
#session state

if "history" not in st.session_state:
    st.session_state.history = []

if "chat" not in st.session_state:
        system_prompt = f"""You are an AI Visual Novel Engine.Story Genre:{genre}Art Style:{art_style}

                            Rules:

                                    Always respond ONLY in valid JSON.

                                    Do NOT use markdown.

                                    Return exactly this format:

                                    {
                                        {      
                                            "story_text":"Story here",

                                            "image_prompt":"Detailed prompt for AI image generation",

                                            "options":[
                                            "Choice 1",
                                            "Choice 2",
                                            "Choice 3"
                                            ]
                                        }
                                    }

                                            The story should be around 80-100 words.

                                            The image_prompt must be detailed.

                                            The options should continue the story naturally.
                                            """
        
system_prompt = f"""
You are an expert AI Visual Novel Engine.

Your task is to create an interactive "Choose Your Own Adventure" story.

Story Genre:
{genre}

Art Style:
{art_style}

RULES:

1. Always continue the story based on the user's previous choice.

2. Keep the story between 80 and 120 words.

3. Make the story engaging, creative, and suitable for all audiences.

4. Generate a highly detailed image prompt describing the current scene.
The image prompt should include:
- Characters
- Environment
- Lighting
- Mood
- Camera angle
- Art Style ({art_style})

5. Always provide exactly THREE unique choices for the next action.

6. The choices should naturally continue the story.

7. Never explain anything outside the JSON.

8. Never use Markdown.

9. Never wrap the response inside ```json or ```.

10. Return ONLY valid JSON.

Return the response exactly in this format:

{{
    "story_text": "Story paragraph here.",
    "image_prompt": "Highly detailed AI image prompt.",
    "options": [
        "Choice 1",
        "Choice 2",
        "Choice 3"
    ]
}}

Ensure the JSON is valid and can be parsed directly using Python's json.loads().
"""    
st.session_state.chat = client.chats.create(model="gemini-2.5-flash",config={"system_instruction": system_prompt})


# -----------------------------
# Start Story
# -----------------------------

if st.button("🚀 Start Story"):

    try:

        response = st.session_state.chat.send_message(f"""Start an exciting {genre} story.Keep it under 100 words.Remember:Return ONLY valid JSON.""")

        # Convert JSON text into Python Dictionary
        data = json.loads(response.text)

        # Save story
        st.session_state.history.append(data)

        st.rerun()

    except json.JSONDecodeError:

        st.error("❌ Gemini returned invalid JSON.")

    except Exception as e:

        st.error(f"Gemini Error: {e}")
# -----------------------------
# Display Story History
# -----------------------------

for i, chapter in enumerate(st.session_state.history):

    st.markdown("---")

    # Story Text
    st.subheader(f"📖 Chapter {i+1}")

    st.write(chapter["story_text"])

    # -----------------------------
    # Image Generation
    # -----------------------------

    try:

        image_url = (
            "https://image.pollinations.ai/prompt/"
            + quote(chapter["image_prompt"])
        )

        st.image(image_url, use_container_width=True)

    except:

        st.toast("🖼️ Image server is busy. Skipping image...")

    # -----------------------------
    # Text To Speech
    # -----------------------------

    try:

        tts = gTTS(chapter["story_text"])

        audio_file = f"story_{i}.mp3"

        tts.save(audio_file)

        st.audio(audio_file)

    except:

        st.toast("🔊 Audio could not be generated.")
        # -----------------------------
# Dynamic Choices
# -----------------------------

if len(st.session_state.history) > 0:

    latest_story = st.session_state.history[-1]

    st.subheader("Choose Your Next Move")

    for option in latest_story["options"]:

        if st.button(option):

            try:

                response = st.session_state.chat.send_message(option)

                data = json.loads(response.text)

                st.session_state.history.append(data)

                st.rerun()

            except json.JSONDecodeError:

                st.error("Invalid JSON received.")

            except Exception as e:

                st.error(e)
# -----------------------------
# Sidebar Controls
# -----------------------------

st.sidebar.markdown("---")

if st.sidebar.button("🔄 Restart Story"):

    # Clear story history
    st.session_state.history = []

    # Create a fresh chat
    system_prompt = f"""
You are an AI Visual Novel Engine.

Story Genre:
{genre}

Art Style:
{art_style}

Always return ONLY valid JSON.

Format:

{{
"story_text":"Story",

"image_prompt":"Detailed image prompt",

"options":[
"Choice 1",
"Choice 2",
"Choice 3"
]
}}
"""

    st.session_state.chat = client.chats.create(
        model="gemini-2.5-flash",
        config={
            "system_instruction": system_prompt
        }
    )

    st.success("Story Restarted!")

    st.rerun()

# -----------------------------
# Footer
# -----------------------------

st.markdown("---")

st.caption(
    "📖 AI Multi-Modal Visual Novel | "
)