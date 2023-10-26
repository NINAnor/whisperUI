# Whisper UI

A user interface to make the use of [whisper](https://github.com/openai/whisper) very easy. 

WhisperUI returnes .srt files (i.e. time-stamped translation / transcription).

# How to use it

Create the docker image:

```
git clone https://github.com/NINAnor/whisperUI
docker build -t whisperui -f Dockerfile .
```

Run the application on `localhost`:

```
docker run --rm -p 8999:8999 whisperui
```
