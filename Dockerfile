FROM python:3.13.13-slim-bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.10.2 /uv /usr/local/bin/uv

WORKDIR /workdays-tool

# Copy dependency files first (better layer caching)
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-cache

# Copy app code
COPY . .

# Default port, user can override
ENV PORT=8501

EXPOSE $PORT

# Run the app
CMD uv run streamlit run main.py --server.port=$PORT --server.address=0.0.0.0
