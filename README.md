# Whisper UI

A user interface to make the use of [whisper](https://github.com/openai/whisper) very easy. 

WhisperUI returnes .srt files (i.e. time-stamped translation / transcription).

# How to use it

Create the docker image:

```
git clone https://github.com/NINAnor/whisperUI
docker build -t whisperui -f Dockerfile .
```

To build with a different Whisper model:

```bash
# Get the model URL using the tool
WHISPER_MODEL_URL=$(uv run python utils/get_model_url.py medium)

# Build with custom model
docker build \
  --build-arg WHISPER_MODEL_URL=$WHISPER_MODEL_URL \
  --build-arg WHISPER_MODEL=medium \
  -t whisperui .
```

Available models: `tiny`, `base`, `small`, `medium`, `large-v1`, `large-v2`, `large-v3`, `turbo`
(Also available with `.en` suffix for English-only versions)

Run the application on `localhost`:

```
docker run --rm -p 8999:8999 whisperui
```
