import whisper
import argparse


def translate(file, language=None):
    model = whisper.load_model("medium")
    if language:
        results = model.transcribe(file, language=language, task="translate")
    else:
        results = model.transcribe(file, task="translate")
    with open("translation.txt", "w", encoding="utf-8") as txt:
        txt.write(results["text"])


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
