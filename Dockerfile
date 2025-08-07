# Use latest CUDA runtime image
FROM nvidia/cuda:12.0.0-cudnn8-runtime-ubuntu22.04

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-venv \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy uv binary from official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Pre-download the Whisper model
ARG WHISPER_MODEL=medium
RUN uv pip install --system faster-whisper
RUN python3 -c "from faster_whisper import WhisperModel; model = WhisperModel('${WHISPER_MODEL}')"

WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies with cache mount
ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Copy application code
COPY . .

ENV STREAMLIT_SERVER_HEADLESS=true
EXPOSE 8501/TCP
CMD ["uv", "run", "streamlit", "run", "app.py"]

