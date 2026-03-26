from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Load once at startup (first run downloads model weights)
classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
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
    import os
    port = int(os.environ.get("PORT","5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
