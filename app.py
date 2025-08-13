import os
import tempfile
from pathlib import Path

import streamlit as st

from utils.whisper import transcribe_and_translate

st.set_page_config(layout="centered", page_title="Whisper Translation App")
st.title("🎧 Whisper-based Translation & Transcription")

st.markdown("""
1. **Upload an `.mp3` file (interview, podcast ...)**
2. **Choose the language of the .mp3 file (by default, automatically detects)**
3. **Click Process**
4. **Download Translation or Transcription**
""")

# Create session directory
if "session_dir" not in st.session_state:
    st.session_state["session_dir"] = tempfile.mkdtemp()

uploaded_file = st.file_uploader("Upload MP3 file", type=["mp3"])

# Language options with explicit names
language_options = {
    "Auto-detect": "auto",
    "Norwegian: no": "no",
    "English: en": "en",
    "French: fr": "fr",
    "German: de": "de",
    "Spanish: es": "es",
    "Italian: it": "it",
    "Finnish: fi": "fi",
    "Russian: ru": "ru",
    "Chinese: zh": "zh",
    "Japanese: ja": "ja",
    "Portuguese: pt": "pt",
    "Swedish: sv": "sv",
}

language_display = st.selectbox(
    "Select language of the file (or leave 'Auto-detect')",
    options=list(language_options.keys()),
)
language = language_options[language_display]

if uploaded_file:
    session_dir = Path(st.session_state["session_dir"])
    audio_path = session_dir / uploaded_file.name

    # Save uploaded file (only once)
    if "audio_path" not in st.session_state:
        with audio_path.open("wb") as f:
            f.write(uploaded_file.read())
        st.session_state["audio_path"] = audio_path

    # Show "Process" button only if we haven't processed yet
    if "trans_path" not in st.session_state and st.button("🚀 Process file"):
        with st.spinner("Transcribing and translating..."):
            trans_path, transl_path, language = transcribe_and_translate(
                st.session_state["audio_path"],
                output_dir=session_dir,
                language=language,
            )
            st.session_state["trans_path"] = trans_path
            st.session_state["transl_path"] = transl_path
        st.success("✅ Processing complete.")

# Show download buttons if processing is complete
if "trans_path" in st.session_state and "transl_path" in st.session_state:
    with Path(st.session_state["trans_path"]).open("rb") as f:
        st.download_button(
            "📄 Download Transcription (SRT)", f, file_name="transcription.srt"
        )

    with Path(st.session_state["transl_path"]).open("rb") as f:
        st.download_button(
            "🌍 Download Translation (SRT)", f, file_name="translation.srt"
        )
