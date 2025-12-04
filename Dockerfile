FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy trained model and inference code
COPY model/ ./model/
COPY code/inference_server.py .

# Expose port
EXPOSE 8080

# Run inference server
CMD ["python", "inference_server.py"]