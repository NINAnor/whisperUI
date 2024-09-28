FROM nvidia/cuda:11.8.0-base-ubuntu22.04

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    python3 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

ARG USE_CUDA=0

# Install PyTorch with or without CUDA support
RUN if [ "$USE_CUDA" = "1" ]; then \
        pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118; \
    else \
        pip3 install torch torchvision torchaudio; \
    fi

# Install other Python dependencies
RUN pip3 install git+https://github.com/openai/whisper.git
RUN pip3 install dash dash-bootstrap-components

WORKDIR /app
COPY ./ .

CMD [ "python3", "app.py" ]

