# 1. Use the target platform for the builder so pip compiles for the right CPU
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies (necessary for compiling some ARM wheels)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install to a local folder
RUN pip install --user --no-cache-dir -r requirements.txt

# 2. Final Image
FROM python:3.11-slim

WORKDIR /app

# Copy the ARM-compiled packages
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
# Streamlit specific env vars
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "app.py"]