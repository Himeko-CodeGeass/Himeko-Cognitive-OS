import os
import logging
import time
import requests
from flask import Flask, request
from google import genai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

genai_client = genai.Client(api_key=GEMINI_API_KEY)
GEMINI_MODEL = "gemini-3.6-flash"

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

@app.route("/")
def index():
    return "Himeko Cognitive OS is running.", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        logger.info(f"收到 Telegram 資料: {data}")

        if "message" in data and "text" in data["message"]:
            chat_id = data["message"]["chat"]["id"]
            user_message = data["message"]["text"]

            reply_text = None
            max_retries = 3
            
            # 自動重試機制，對應 503 伺服器忙碌
            for attempt in range(max_retries):
                try:
                    response = genai_client.models.generate_content(
                        model=GEMINI_MODEL,
                        contents=user_message,
                    )
                    reply_text = response.text
                    break
                except Exception as api_err:
                    logger.warning(f"第 {attempt + 1} 次呼叫 Gemini 失敗: {api_err}")
                    if attempt < max_retries - 1:
                        time.sleep(2) # 等待 2 秒後重試
                    else:
                        reply_text = "伺服器目前流量較大，請稍後再試一次。"

            # 透過 Telegram Bot API 回傳訊息
            requests.post(TELEGRAM_API_URL, json={
                "chat_id": chat_id,
                "text": reply_text
            })

        return "OK", 200
    except Exception as e:
        logger.error(f"Webhook 錯誤: {e}")
        return str(e), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
