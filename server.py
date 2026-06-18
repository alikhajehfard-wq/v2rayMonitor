from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)


@app.route("/")
def home():
    return "V2ray Monitor API Running"


@app.route("/api")
def api():
    url = request.args.get("url")

    try:
        r = requests.get(url, timeout=10)
        text = r.text

        # پیدا کردن مقدار GB
        match = re.search(r"(\d+(\.\d+)?)\s*GB", text)

        if not match:
            return jsonify({"error": "not found"})

        remaining = float(match.group(1))

        return jsonify({"remaining": remaining})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
