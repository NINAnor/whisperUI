FROM python:3.10

# Pre-download Whisper model using ADD
ARG WHISPER_MODEL_URL=https://openaipublic.azureedge.net/main/whisper/models/345ae4da62f9b3d59415adc60127b97c714f32e89e936602e85993674d08dcb1/medium.pt
ARG WHISPER_MODEL=medium
RUN mkdir -p /root/.cache/whisper
ADD ${WHISPER_MODEL_URL} /root/.cache/whisper/${WHISPER_MODEL}.pt

# Remove apt auto-clean hook to preserve cache
RUN rm -f /etc/apt/apt.conf.d/docker-clean

# Install system dependencies with cache mount
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=type=cache,target=/var/lib/apt/lists \
    apt update && apt install -y --no-install-recommends ffmpeg

# Copy uv binary
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies with cache mount
ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Copy application code
COPY . .

CMD ["uv", "run", "python", "app.py"]
