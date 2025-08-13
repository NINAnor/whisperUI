# Use latest CUDA runtime image
FROM nvidia/cuda:12.0.0-cudnn8-runtime-ubuntu22.04

# Copy uv binary from official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy and install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Copy application code
COPY . .

# Download Whisper model during build
ARG WHISPER_MODEL=medium
RUN uv run python3 -c "from faster_whisper import WhisperModel; WhisperModel('${WHISPER_MODEL}')"

CMD ["uv", "run", "streamlit", "run", "app.py"]
