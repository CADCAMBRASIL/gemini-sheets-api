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

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-001:generateContent?key={API_KEY}"


    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": prompt}]}
        ]
    }

    r = requests.post(url, json=payload, timeout=60)
    data = r.json()

    # 🔍 Extrair texto de forma segura
    if "candidates" not in data:
        return jsonify({"text": "⚠️ Erro da API Gemini:\n" + str(data)})

    parts = data["candidates"][0]["content"].get("parts", [])
    text = "\n".join(p.get("text", "") for p in parts).strip()

    if not text:
        return jsonify({"text": "⚠️ Gemini respondeu sem texto útil."})

    return jsonify({"text": text})


@app.get("/")
def health():
    return "ok"
