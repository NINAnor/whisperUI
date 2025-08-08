# Whisper UI

A user interface to make the use of [whisper](https://github.com/openai/whisper) very easy.

WhisperUI returns .srt files (i.e. time-stamped translation / transcription).

## Setup
Install `uv`: https://docs.astral.sh/uv/getting-started/installation/

```bash
uv sync
uv run pre-commit install # optional
```

### Run
To execute the application run:
```
uv run streamlit run app.py
```

### Development
Just run `uv run streamlit run app.py` and you are good to go!

### (Optional) pre-commit
pre-commit is a set of tools that help you ensure code quality. It runs every time you make a commit.
To install pre-commit hooks run:
```bash
uv run pre-commit install
```

### How to install a package
Run `uv add <package-name>` to install a package. For example:
```bash
uv add requests
```

#### Visual studio code
If you are using visual studio code install the recommended extensions

### Development with docker
A basic docker image is already provided, run:
```bash
docker compose up --build watch
```

### Docker usage
Create the docker image:

```
git clone https://github.com/NINAnor/whisperUI
docker build -t whisperui -f Dockerfile .
```

Run the application on `localhost`:

```
docker run --rm -p 8501:8501 whisperui
```

### Tools installed
- uv
- pre-commit (optional)
