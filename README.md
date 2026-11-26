# Whisper UI

A user interface to make the use of [whisper](https://github.com/openai/whisper) very easy.

WhisperUI returns .srt files (i.e. time-stamped translation / transcription).

## Setup
Install `uv`: https://docs.astral.sh/uv/getting-started/installation/

```bash
uv sync --dev
uv run pre-commit install # optional

### Run
To execute the application run:
```
uv run streamlit run app.py
```

### Development
Just run `uv run streamlit run app.py` and you are good to go!

### Update from template
To update your project with the latest changes from the template, run:
```bash
uvx --with copier-template-extensions copier update --trust
```

You can keep your previous answers by using:
```bash
uvx --with copier-template-extensions copier update --trust --defaults
```

### (Optional) pre-commit
pre-commit is a set of tools that help you ensure code quality. It runs every time you make a commit.

First, install dependencies:
```bash
uv sync --dev
```

Then install pre-commit hooks:
```bash
uv run pre-commit install
```

To run pre-commit on all files:
```bash
uv run pre-commit run --all-files
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

### Docker Compose device and CPU threads

By default, Docker Compose runs without requesting a GPU and `faster-whisper`
automatically selects an available device. Set these variables in a `.env` file
to force CPU execution and choose the number of CPU threads:

```env
WHISPER_DEVICE=cpu
WHISPER_CPU_THREADS=4
```

`WHISPER_CPU_THREADS=0` lets the runtime choose the thread count. Start the app
with `docker compose up --build`.

To run with a GPU, start the opt-in GPU service instead:

```bash
docker compose --profile gpu up --build whisperui-gpu
```

Set `WHISPER_DEVICE=cuda` in `.env` to explicitly select CUDA, or leave it as
`auto` to let the model choose.

### Tools installed
- uv
- pre-commit (optional)
