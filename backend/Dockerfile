# Build stage
FROM python:3.9-slim as builder
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9-slim
COPY --from=builder /opt/venv /opt/venv
WORKDIR /app
COPY . .
ENV PATH="/opt/venv/bin:$PATH"
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "src.fastapi_app.main:app", "--host", "0.0.0.0", "--port", "8000"]