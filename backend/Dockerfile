FROM python:3.12-slim

# Set workdir
WORKDIR /app

# Install deps
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY app/ .

# Run FastAPI
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000 > /dev/null"]
