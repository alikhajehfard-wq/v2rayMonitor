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
        r = requests.get(url, timeout=15)
        text = r.text

        # 🔥 مهم: دنبال Remained / Remaining / Usage / Total
        patterns = [
            r"Remained\s*</td>\s*<td[^>]*>(\d+(?:\.\d+)?)\s*GB",
            r"Remaining\s*</td>\s*<td[^>]*>(\d+(?:\.\d+)?)\s*GB",
            r"(\d+(?:\.\d+)?)\s*GB",
        ]

        remaining = None

        for p in patterns:
            match = re.search(p, text, re.IGNORECASE)
            if match:
                remaining = float(match.group(1))
                break

        if remaining is None:
            return jsonify({"status": "not_found", "debug_sample": text[:1000]})

        return jsonify({"status": "ok", "remaining": remaining})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
