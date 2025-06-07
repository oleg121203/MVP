# Base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Create a non-root user and group
# Using a fixed UID/GID is good practice for consistency
RUN groupadd -g 1001 appgroup && useradd --no-log-init -r -g appgroup -u 1001 appuser

# Set working directory
WORKDIR /app

# Create virtual environment
# Ensure python3 points to the correct version if multiple are somehow present
RUN python3 -m venv /app/venv
# Add venv to PATH for subsequent RUN, CMD, ENTRYPOINT instructions
ENV PATH="/app/venv/bin:$PATH"

# Install system dependencies (if any are needed for your packages)
# Example:
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     libpq-dev gcc \
#     && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

# Install Python dependencies into the virtual environment
# Ensure pip from venv is used
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Explicitly install packages that have caused issues, as a safeguard
# This is a fallback; ideally, requirements.txt should be the single source of truth.
RUN pip install pandas==2.2.2 scikit-learn==1.3.2

# Copy the rest of the application code
# This should come after dependency installation to optimize caching
COPY . /app/

# Change ownership of the /app directory to the non-root user
# This ensures the appuser can write to logs or other necessary files if needed
RUN chown -R appuser:appgroup /app

# Switch to the non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Healthcheck (adjust path and port if your app's health endpoint is different)
# The command in docker-compose.yml will start uvicorn on 0.0.0.0:8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD wget -qO- http://localhost:8000/docs || exit 1
  # Or use a dedicated /health endpoint if you have one:
  # CMD wget -qO- http://localhost:8000/health || exit 1

# The CMD to run the application will be in docker-compose.dev.yml
# Example: CMD ["python", "-m", "uvicorn", "src.fastapi_app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]