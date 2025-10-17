# Use Python 3.11 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Create app user for security
RUN useradd --create-home --shell /bin/bash appuser

# Set working directory
WORKDIR /home/appuser/app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        unixodbc \
        unixodbc-dev \
        freetds-dev \
        freetds-bin \
        tdsodbc \
    && rm -rf /var/lib/apt/lists/*

# Install UV using the official method - copy from the official uv image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files
COPY pyproject.toml uv.lock* README.md ./

# Install dependencies using UV with optimizations (without frozen to allow new deps)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-install-project

# Copy application code
COPY app/ ./app/

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# Change ownership to app user
RUN chown -R appuser:appuser /home/appuser
USER appuser

# Create uploads directory
RUN mkdir -p uploads

# Place the virtual environment at the front of the PATH
ENV PATH="/home/appuser/app/.venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Start the application using the virtual environment directly with large file support
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "300", "--limit-concurrency", "1000"]