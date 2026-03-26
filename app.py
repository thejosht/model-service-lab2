import os

from flask import Flask, request, jsonify
from dotenv import load_dotenv
from transformers import pipeline

# Load environment variables from .env (local) if present
# NOTE: .env is ignored by git; .env.example is safe to commit.
load_dotenv()

app = Flask(__name__)

HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
PORT = int(os.getenv("PORT", "5000"))

# Load once at startup (first run downloads model weights)
# If HF_TOKEN is set, it will be used to authenticate downloads (private models / higher rate limits).
classifier_kwargs = {}
if HF_TOKEN:
    classifier_kwargs["token"] = HF_TOKEN

classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    **classifier_kwargs
)

@app.get("/health")
def health():
    return jsonify(status="ok")

@app.post("/predict")
def predict():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")

    if not isinstance(text, str) or not text.strip():
        return jsonify(error="Please provide non-empty 'text' (string)."), 400

    pred = classifier(text, truncation=True)[0]
    return jsonify(
        input=text,
        label=pred["label"],
        score=float(pred["score"])
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT, debug=True)
