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
        # گرفتن صفحه
        r = requests.get(url, timeout=15)
        text = r.text

        # --- پیدا کردن همه GB ها (قوی و مطمئن) ---
        matches = re.findall(r"(\d+(?:\.\d+)?)\s*GB", text)

        # اگر پیدا نشد
        if not matches:
            return jsonify({"status": "not_found", "debug_sample": text[:800]})

        # اولین مقدار را می‌گیریم (remaining)
        remaining = float(matches[0])

        return jsonify({"status": "ok", "remaining": remaining})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
