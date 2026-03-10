import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv
from audio_recorder_streamlit import audio_recorder
import tempfile

# environment variables
load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

st.set_page_config(page_title="WrenchMate AI", page_icon="🔧")

st.title("🔧 WrenchMate AI")
st.subheader("Your NLP-Driven Interactive Service Manual")

# 1. Setup the Sidebar for Voice Input
with st.sidebar:
    st.write("🎤 **Voice Command**")
    st.write("Click the mic to record, click again to stop.")
    audio_bytes = audio_recorder(text="", icon_size="2x")

# 2. Sys Engineering
system_prompt = """
You are WrenchMate, an expert AI mechanic assistant. 
Keep answers concise, step-by-step, and bulleted.
Emphasize safety first (e.g., disconnecting the battery, using jack stands).
If asked about a 2009 Toyota Avalon or 2007 RAV4, provide highly specific bolt sizes and torque specs.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 3. Handle the Input (Voice or Text)
prompt = None

# Check if new audio was recorded
if audio_bytes and audio_bytes != st.session_state.get("last_audio"):
    st.session_state.last_audio = audio_bytes # Prevent endless transcription loops
    
    # Save recorded audio to a temporary file for Whisper
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes)
        temp_audio_path = temp_audio.name

    # Send to OpenAI Whisper for transcription
    with st.spinner("Transcribing audio..."):
        with open(temp_audio_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        prompt = transcript.text
    
    os.remove(temp_audio_path)

# Check if text was typed (Fallback)
text_input = st.chat_input("E.g., How do I remove the front fender on a 2009 Avalon?")
if text_input:
    prompt = text_input

# 4. AI Response
if prompt:
    # Show user message
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Get and show AI response
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    
    st.session_state.messages.append({"role": "assistant", "content": response})