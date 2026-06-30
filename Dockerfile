# Backend Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 8000
RUN useradd -m myuser
USER myuser
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
