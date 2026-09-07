# -*- coding: utf-8 -*-
import os
import sys
from flask import Flask, request
from core.gestalt_engine import GestaltEngine

# 確保專案根目錄納入 Python 搜尋路徑
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

app = Flask(__name__)
engine = GestaltEngine()

@app.route("/", methods=["GET"])
def index():
    return "Himeko Cognitive OS is running.", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    if data:
        # 這裡之後會對接 Telegram 訊息處理邏輯
        pass
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
