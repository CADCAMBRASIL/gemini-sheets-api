from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("GEMINI_API_KEY")

@app.route("/gemini", methods=["POST"])
def gemini():
    prompt = (request.json or {}).get("prompt", "").strip()

    if not prompt:
        return jsonify({"text": "⚠️ Prompt vazio recebido."})

    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={API_KEY}"


    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": prompt}]}
        ]
    }

    r = requests.post(url, json=payload, timeout=60)
    data = r.json()

    # 🔍 Tratamento de erro do Gemini
    if "candidates" not in data:
        return jsonify({
            "text": "⚠️ Erro da API Gemini:\n" + str(data)
        })

    text = data["candidates"][0]["content"]["parts"][0]["text"]
    return jsonify({"text": text})

@app.get("/")
def health():
    return "ok"
