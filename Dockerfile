FROM python:3.8

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
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

# Copy application code
COPY . .

# Pre-download Whisper model to avoid runtime download
RUN uv run python -c "import whisper; whisper.load_model('medium')"

CMD ["uv", "run", "python", "app.py"]
