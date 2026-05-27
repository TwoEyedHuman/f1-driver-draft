# Stage 1 — Builder: install Python deps
FROM python:3.12-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --user --no-cache-dir --no-compile -r requirements.txt && \
    find /root/.local -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Stage 2 — Runner: lean image with app + data
FROM python:3.12-slim

# Non-root user
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /home/appuser/app

# Copy compiled deps from builder into appuser home
COPY --from=builder /root/.local /home/appuser/.local

# Copy all app and data files
COPY --chown=appuser:appuser . .

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/home/appuser/app
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

ENTRYPOINT ["streamlit", "run", "app/main.py"]
