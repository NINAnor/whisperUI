import whisper
import argparse

def translate(file):

    model = whisper.load_model('medium')
    results = model.transcribe(file, language="no", task="translate")
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
    
    cli_args = parser.parse_args()
    
    translate(cli_args.input)

