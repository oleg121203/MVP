# Build stage
FROM python:3.9-slim AS builder
WORKDIR /app

# Create and activate virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install dependencies
COPY requirements.txt .
RUN /opt/venv/bin/pip install --no-cache-dir -r requirements.txt
RUN /opt/venv/bin/pip install scikit-learn==1.3.2
RUN /opt/venv/bin/pip install pandas==2.2.2

# Runtime stage
FROM python:3.9-slim
COPY --from=builder /opt/venv /opt/venv
WORKDIR /app
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["/opt/venv/bin/python", "src/fastapi_app/main.py", "--reload"]