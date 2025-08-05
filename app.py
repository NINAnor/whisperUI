import streamlit as st
import tempfile
import os
import shutil
from utils.whisper import transcribe_and_translate

st.set_page_config(layout="centered", page_title="Whisper Translation App")
st.title("🎧 Whisper-based Translation & Transcription")

st.markdown("""
1. **Upload a Norwegian `.mp3` file**
2. **Click Process**
3. **Download Translation or Transcription**
""")

# Create a per-session directory if not already present
if "session_dir" not in st.session_state:
    st.session_state["session_dir"] = tempfile.mkdtemp()

uploaded_file = st.file_uploader("Upload MP3 file", type=["mp3"])

if uploaded_file:
    session_dir = st.session_state["session_dir"]
    audio_path = os.path.join(session_dir, uploaded_file.name)

    # Save uploaded audio to session-specific directory
    with open(audio_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("File uploaded successfully.")

    if st.button("Process"):
        with st.spinner("Transcribing and translating..."):
            trans_path, transl_path = transcribe_and_translate(audio_path, output_dir=session_dir)

        with open(trans_path, "rb") as f:
            st.download_button("📄 Download Transcription (SRT)", f, file_name="transcription.srt")

        with open(transl_path, "rb") as f:
            st.download_button("🌍 Download Translation (SRT)", f, file_name="translation.srt")

        st.success("Done!")