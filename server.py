from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)


@app.route("/")
def home():
    return "V2ray Monitor Running"


@app.route("/api")
def api():

    url = request.args.get("url")

    if not url:
        return jsonify({"status": "error", "message": "no url"})

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
        }

        r = requests.get(url, headers=headers, timeout=20)
        text = r.text

        # 🚀 1. بهترین حالت: مستقیم از data-remained
        match = re.search(r'data-remained="([\d.]+)GB"', text)

        if match:
            return jsonify({"status": "ok", "remaining": float(match.group(1))})

        # 🚀 2. fallback: Remained داخل HTML
        match = re.search(r"Remained.*?(\d+(?:\.\d+)?)\s*GB", text, re.IGNORECASE)

        if match:
            return jsonify({"status": "ok", "remaining": float(match.group(1))})

        # 🚀 3. fallback آخر
        match = re.search(r"(\d+(?:\.\d+)?)\s*GB", text)

        if match:
            return jsonify({"status": "ok", "remaining": float(match.group(1))})

        return jsonify({"status": "not_found", "debug_sample": text[:800]})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
