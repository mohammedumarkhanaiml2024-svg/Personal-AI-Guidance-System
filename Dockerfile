# Multi-stage Dockerfile for Personal AI Guidance System
FROM python:3.12-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application files
COPY main_enhanced.py .
COPY auth.py .
COPY models.py .
COPY schemas.py .
COPY database.py .
COPY utils.py .
COPY ai_service.py .
COPY google_ai_service.py .
COPY brain_service.py .
COPY private_data_store.py .
COPY data_privacy_service.py .

# Copy frontend files
COPY *.html .
COPY *.css .
COPY *.js .

# Create necessary directories
RUN mkdir -p private_user_data user_brains logs

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH=/root/.local/bin:$PATH

# Expose ports
EXPOSE 8000 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "main_enhanced:app", "--host", "0.0.0.0", "--port", "8000"]
