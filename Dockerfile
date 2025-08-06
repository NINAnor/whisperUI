FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

FROM base AS model-downloader

ARG WHISPER_MODEL=medium
RUN uv pip install --system faster-whisper
RUN python -c "from faster_whisper import WhisperModel; model = WhisperModel('${WHISPER_MODEL}', device='cpu')"

FROM base

# Copy model cache from first stage
COPY --from=model-downloader /root/.cache /root/.cache

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
