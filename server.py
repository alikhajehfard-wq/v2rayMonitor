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

        # 🔥 1. اول دنبال Remained / Remaining / Usage
        patterns = [
            r"Remained[^0-9]{0,10}(\d+(?:\.\d+)?)\s*GB",
            r"Remaining[^0-9]{0,10}(\d+(?:\.\d+)?)\s*GB",
            r"(\d+(?:\.\d+)?)\s*GB",
        ]

        value = None

        for p in patterns:
            m = re.search(p, text, re.IGNORECASE)
            if m:
                value = float(m.group(1))
                break

        # 🔥 2. اگر بالا نگرفت → از آخرین عدد GB در صفحه استفاده کن
        if value is None:
            all_matches = re.findall(r"(\d+(?:\.\d+)?)\s*GB", text)
            if all_matches:
                value = float(all_matches[-1])  # آخرین عدد (معمولاً Remained است)

        if value is None:
            return jsonify({"status": "not_found", "debug_sample": text[:800]})

        return jsonify({"status": "ok", "remaining": value})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
