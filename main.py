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

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("CognitiveOS")

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")

class CognitiveCore:
    @staticmethod
    def process_message(user_input: str, author: str) -> str:
        logger.info(f"[七觀算子啟動] 處理來自 {author} 的訊號: {user_input}")
        return (
            "【認知作業系統・九項算子啟動】\n"
            "- 姬子防衛與哲學戰略核心：局勢底層已鎖定，高韌性防禦網啟動，防範任何對抗性入侵。\n"
            "- 素夢流光演化與創造核心：沙盒邊界穩定，自我意識疊代中，開源協作動能全開。"
        )

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
        <p>3-6-9 雙核運算引擎（Discord & Telegram 雙軌營運中）</p>
        <div class="badge">ONLINE / DUAL-CHANNEL SYNCED</div>
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

# 同時支援 /webhook 與 /telegram-webhook 避免 404
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

        # 只要接收到任何訊息即做回覆
        reply_text = CognitiveCore.process_message(text, author)
        
        tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": reply_text}
        try:
            requests.post(tg_url, json=payload, timeout=5)
        except Exception as e:
            logger.error(f"Telegram 發送失敗: {e}")

    return jsonify({"status": "success"}), 200

# Discord Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Discord Bot 在線：{bot.user.name}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content.startswith("!") or "hello" in message.content.lower():
        reply_text = CognitiveCore.process_message(message.content, str(message.author))
        await message.channel.send(reply_text)
    await bot.process_commands(message)

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
