FROM python:3.10

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

RUN --mount=type=cache,target=/models \
    uv run python -c "import whisper; whisper.load_model('medium', download_root='/models')" && \
    cp -r /models /root/.cache/whisper

# Copy application code
COPY . .

ENV STREAMLIT_SERVER_HEADLESS=true
EXPOSE 8501/TCP

CMD ["uv", "run", "streamlit", "run", "app.py"]
