# Build stage
FROM python:3.9-slim AS builder

WORKDIR /app

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9-slim

# Create non-root user for security
RUN useradd -m -u 1000 appuser
USER appuser

WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Healthcheck for the application
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://localhost:8000/health || exit 1

# Command to run the application
CMD ["/opt/venv/bin/python", "src/fastapi_app/main.py"]