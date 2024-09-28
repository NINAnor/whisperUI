# Whisper UI

A user interface to make the use of [whisper](https://github.com/openai/whisper) very easy. 

WhisperUI returnes .srt files (i.e. time-stamped translation / transcription).

# How to use it

Create the docker image:

```
git clone https://github.com/NINAnor/whisperUI
# For CUDA support:
docker build --build-arg USE_CUDA=1 -t whisperui:cuda .
# For CPU-only:
docker build --build-arg USE_CUDA=0 -t whisperui:cpu .
```

Run the application on `localhost`:

```
# For CUDA support:
docker run --rm -p 8999:8999 whisperui:cuda
# For CPU-only:
docker run --rm -p 8999:8999 whisperui:cpu
```
