from .srt import write_srt
import os
import whisper

def transcribe_and_translate(file_path, output_dir="."):
    model = whisper.load_model("medium")

    transcription = model.transcribe(file_path, language="no")
    translation = model.transcribe(file_path, language="no", task="translate")

    trans_path = os.path.join(output_dir, "transcription.srt")
    transl_path = os.path.join(output_dir, "translation.srt")

    write_srt(transcription["segments"], trans_path)
    write_srt(translation["segments"], transl_path)

    return trans_path, transl_path