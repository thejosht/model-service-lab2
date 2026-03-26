# HuggingFace Sentiment Model Service (Flask + Docker)

This project serves a pretrained HuggingFace model through a REST API and is packaged with Docker.

## Pretrained Model

- `distilbert-base-uncased-finetuned-sst-2-english` (sentiment classification)

## API Endpoints

- `GET /health`  
  Returns: `{"status":"ok"}`
- `POST /predict`  
  Body: `{"text":"..."}`
  Returns: `{"input":"...","label":"POSITIVE|NEGATIVE","score":...}`

## Build and Run Locally (Docker)

### 1) Build the image

```bash
docker build -t model-service:latest .

### 2) Run the container

docker run --rm -e PORT=5000 -p 5050:5000 model-service:latest

### 3) Test the API

curl -s http://localhost:5050/health
curl -s -X POST http://localhost:5050/predict \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello from Docker"}'

### Info
	•	Repo: https://hub.docker.com/r/thejosht/model-service
	•	Image tag: thejosht/model-service:latest
```
