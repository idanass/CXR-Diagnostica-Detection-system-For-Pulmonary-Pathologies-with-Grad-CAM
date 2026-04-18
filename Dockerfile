FROM python:3.11

WORKDIR /app

# Install PyTorch first (CPU version, Linux)
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    python-multipart \
    torchxrayvision \
    scikit-image \
    matplotlib \
    pillow \
    reportlab \
    minio \
    mlflow \
    prometheus-fastapi-instrumentator

# Copy and install requirements (for anything else)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]