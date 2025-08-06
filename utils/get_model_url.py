#!/usr/bin/env python3
"""
Tool to print Whisper model URLs for Docker builds.
Usage: python get_model_url.py [model_name]
"""
import sys
import whisper

def main():
    model_name = sys.argv[1] if len(sys.argv) > 1 else "medium"
    
    try:
        url = whisper._MODELS[model_name]
        print(url)
    except KeyError:
        print(f"Error: Model '{model_name}' not found.", file=sys.stderr)
        print("Available models:", ", ".join(whisper.available_models()), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()