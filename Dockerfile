FROM python:3.8

RUN apt update && apt install -y --no-install-recommends \
	  ffmpeg

RUN pip install git+https://github.com/openai/whisper.git 
RUN pip install dash
RUN pip install dash-bootstrap-components
	  
WORKDIR /app
COPY ./ .

CMD [ "python", "app.py" ]


