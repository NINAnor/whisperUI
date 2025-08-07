import streamlit as st
import tempfile
import os
import shutil
from utils.whisper import transcribe_and_translate
from utils.qa_chain import build_qa_chain

import os
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

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
language = st.selectbox(
    "Select language of the file (or leave 'Auto')",
    options=["auto", "no", "en", "fr", "de", "es", "it", "fi", "ru", "zh", "ja", "pt", "sv"]
)

if uploaded_file:
    session_dir = st.session_state["session_dir"]
    audio_path = os.path.join(session_dir, uploaded_file.name)

    # Save uploaded file (only once)
    if "audio_path" not in st.session_state:
        with open(audio_path, "wb") as f:
            f.write(uploaded_file.read())
        st.session_state["audio_path"] = audio_path

    # Show "Process" button only if we haven't processed yet
    if "trans_path" not in st.session_state and st.button("🚀 Process file"):
        with st.spinner("Transcribing and translating..."):
            trans_path, transl_path, language = transcribe_and_translate(st.session_state["audio_path"], output_dir=session_dir, language=language)
            st.session_state["trans_path"] = trans_path
            st.session_state["transl_path"] = transl_path
        st.success("✅ Processing complete.")

# Show download buttons if processing is complete
if "trans_path" in st.session_state and "transl_path" in st.session_state:
    with open(st.session_state["trans_path"], "rb") as f:
        st.download_button("📄 Download Transcription (SRT)", f, file_name="transcription.srt")

    with open(st.session_state["transl_path"], "rb") as f:
        st.download_button("🌍 Download Translation (SRT)", f, file_name="translation.srt")

# Chatbot section
if st.checkbox("💬 Chat with the Transcription"):
    if "trans_path" not in st.session_state:
        st.error("❌ Please process a file first before chatting.")
    else:
        with open(st.session_state["trans_path"], "r", encoding="utf-8") as f:
            transcript_text = f.read()

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        if "qa_chain" not in st.session_state:
            with st.spinner("Initializing chatbot..."):
                st.session_state.qa_chain = build_qa_chain(transcript_text)

        user_input = st.text_input("Ask a question about the transcription")

        if user_input:
            result = st.session_state.qa_chain({
                "question": user_input,
                "chat_history": st.session_state.chat_history
            })
            st.session_state.chat_history.append((user_input, result["answer"]))

        for q, a in st.session_state.chat_history:
            st.markdown(f"**You:** {q}")
            st.markdown(f"**Bot:** {a}")
