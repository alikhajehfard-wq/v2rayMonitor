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
        # 🔥 مهم: شبیه مرورگر شدن
        headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"
        }

        r = requests.get(url, headers=headers, timeout=20, allow_redirects=True)

        text = r.text

        # اگر هنوز base64 بود یعنی HTML نگرفته
        if "vless://" in text or len(text) < 200:
            return jsonify({"status": "not_html", "debug_sample": text[:500]})

        # استخراج GB
        match = re.search(r"Remained.*?(\d+(?:\.\d+)?)\s*GB", text, re.IGNORECASE)

        if not match:
            match = re.search(r"(\d+(?:\.\d+)?)\s*GB", text)

        if not match:
            return jsonify({"status": "not_found", "debug_sample": text[:1000]})

        remaining = float(match.group(1))

        return jsonify({"status": "ok", "remaining": remaining})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
