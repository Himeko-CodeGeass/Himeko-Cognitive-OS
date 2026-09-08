import os
import sys
import logging
import threading
import time
import asyncio
import requests
from flask import Flask, request, jsonify, render_template_string
import discord
from discord.ext import commands
import google.generativeai as genai

# ---------------------------------------------------------
# 日誌與環境變數設定
# ---------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("CognitiveOS")

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ---------------------------------------------------------
# Gemini AI 引擎設定
# ---------------------------------------------------------
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # 修正模型名稱：移除 -latest 後綴，改用標準穩定名稱以避免 v1beta 404 錯誤
    model = genai.GenerativeModel("gemini-1.5-pro")


else:
    model = None
    logger.warning("未偵測到 GEMINI_API_KEY，將無法啟用動態 AI 回應功能。")

class CognitiveCore:
    @staticmethod
    def generate_ai_response(user_input: str, author: str) -> str:
        logger.info(f"[AI 算子啟動] 處理來自 {author} 的訊息: {user_input}")
        
        if not model:
            return "【系統提示】GEMINI_API_KEY 未設定，無法呼叫 AI 運算引擎。"

        try:
            prompt = (
                f"系統指令: 你是姬子與素夢流光雙核運算架構下的認知作業系統助理（Jansuchen）。"
                f"請以專業、高質感且條理分明的方式回答主公的問題。\n"
                f"使用者 ({author}): {user_input}"
            )
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            logger.error(f"Gemini API 呼叫失敗: {e}")
            return f"【系統異常】AI 運算發生錯誤：{e}"

# ---------------------------------------------------------
# Flask Web 應用程式 (Flask + Telegram Webhook)
# ---------------------------------------------------------
app = Flask(__name__)

STATUS_HTML = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <title>3-6-9 雙核運算引擎狀態</title>
    <style>
        body { font-family: system-ui, sans-serif; background-color: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background-color: #1e293b; border-radius: 12px; padding: 32px; box-shadow: 0 10px 25px rgba(0,0,0,0.5); text-align: center; border: 1px solid #334155; }
        h1 { color: #38bdf8; margin-bottom: 8px; }
        p { color: #94a3b8; font-size: 1.1em; }
        .badge { display: inline-block; background-color: #10b981; color: #111827; font-weight: bold; padding: 6px 16px; border-radius: 9999px; font-size: 0.9em; margin-top: 12px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>姬子 & 素夢流光</h1>
        <p>3-6-9 雙核運算引擎（AI 動態對話模式已啟用）</p>
        <div class="badge">ONLINE / AI ACTIVE</div>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(STATUS_HTML)

@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"}), 200

@app.route("/webhook", methods=["POST"])
@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error"}), 400

    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
        author = data["message"]["from"].get("username", "TelegramUser")

        reply_text = CognitiveCore.generate_ai_response(text, author)

        tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": reply_text}
        try:
            requests.post(tg_url, json=payload, timeout=10)
        except Exception as e:
            logger.error(f"Telegram 發送失敗: {e}")

    return jsonify({"status": "success"}), 200

# ---------------------------------------------------------
# Discord Bot 邏輯
# ---------------------------------------------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Discord Bot 已成功線上：{bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # 全面接收 Discord 頻道內的語句或以 ! 開頭的指令
    user_text = message.content
    if user_text.startswith("!"):
        user_text = user_text[1:].strip()

    if user_text:
        async with message.channel.typing():
            # 將同步作業交由執行緒池，防範非同步迴圈卡死
            loop = asyncio.get_running_loop()
            reply_text = await loop.run_in_executor(
                None, CognitiveCore.generate_ai_response, user_text, str(message.author)
            )
            await message.channel.send(reply_text)

def run_discord_bot():
    if not DISCORD_BOT_TOKEN:
        logger.error("未找到 DISCORD_BOT_TOKEN！")
        return
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(bot.start(DISCORD_BOT_TOKEN))
    except Exception as e:
        logger.error(f"Discord 啟動失敗: {e}")

# ---------------------------------------------------------
# 防休眠心跳機制
# ---------------------------------------------------------
def keep_alive():
    time.sleep(10)
    base_url = os.getenv("RENDER_EXTERNAL_URL")
    if base_url:
        if not base_url.startswith("http"):
            base_url = f"https://{base_url}"
        while True:
            try:
                requests.get(base_url, timeout=5)
            except Exception:
                pass
            time.sleep(240)

if __name__ == "__main__":
    threading.Thread(target=run_discord_bot, daemon=True).start()
    threading.Thread(target=keep_alive, daemon=True).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
