# Dockerfile
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create config directory
RUN mkdir -p /app/config

# Create a non-root user and switch to it
RUN useradd -m crawler && chown -R crawler:crawler /app
USER crawler

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV CRAWLER_CONFIG=/app/config/crawler_config.yml

# Run the crawler
ENTRYPOINT ["python", "-m", "crawler.run"]
