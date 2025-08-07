from faster_whisper import WhisperModel
import argparse


def translate(file, language=None):
    model = WhisperModel("medium")
    if language:
        segments, info = model.transcribe(file, language=language, task="translate")
    else:
        segments, info = model.transcribe(file, task="translate")
    
    # Extract text from segments
    full_text = " ".join([seg.text for seg in segments])
    
    with open("translation.txt", "w", encoding="utf-8") as txt:
        txt.write(full_text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        help="Path to the file to analyze",
        required=True,
        type=str,
    )
    
    parser.add_argument(
        "--language",
        help="Source language code (e.g., 'no', 'en', 'fr'). If not specified, auto-detect will be used.",
        required=False,
        type=str,
        default=None,
    )

    cli_args = parser.parse_args()

    translate(cli_args.input, cli_args.language)
