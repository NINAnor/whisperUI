from .srt import write_srt
import os
from faster_whisper import WhisperModel

def transcribe_and_translate(file_path, output_dir=".", language="auto"):
    model = WhisperModel("medium", device='auto')

    # Auto-detect language if not specified
    if language == "auto":
        _, info = model.transcribe(file_path, language=None, task="transcribe")
        language = info.language 

    # Get translation segments
    translation_segments, _ = model.transcribe(
        file_path, language=language, task="translate"
    )
    translation = {
        "segments": [
            {"start": seg.start, "end": seg.end, "text": seg.text}
            for seg in translation_segments
        ]
    }

    # Get transcription segments
    transcription_segments, _ = model.transcribe(file_path, language="no")
    transcription = {
        "segments": [
            {"start": seg.start, "end": seg.end, "text": seg.text}
            for seg in transcription_segments
        ]
    }

    trans_path = os.path.join(output_dir, "transcription.srt")
    transl_path = os.path.join(output_dir, "translation.srt")

    write_srt(transcription["segments"], trans_path)
    write_srt(translation["segments"], transl_path)

    return trans_path, transl_path, language