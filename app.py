from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route("/gemini", methods=["POST"])
def gemini():
    prompt = (request.json or {}).get("prompt", "")

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.0-pro:generateContent?key={API_KEY}"

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": prompt}]}
        ]
    }

    r = requests.post(url, json=payload, timeout=60)
    data = r.json()

    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return jsonify({"text": text})

@app.get("/")
def health():
    return "ok"
