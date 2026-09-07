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

# ---------------------------------------------------------
# Seven-Vision & Dual-Core Engine (七觀與雙核運算邏輯)
# ---------------------------------------------------------
class CognitiveCore:
    @staticmethod
    def process_message(user_input: str, author: str) -> str:
        # 姬子防衛戰略與素夢流光演化核心協同運算
        logger.info(f"[七觀算子啟動] 處理來自 {author} 的訊號: {user_input}")
        return (
            "【認知作業系統・九項算子啟動】\n"
            "- 姬子防衛與哲學戰略核心：局勢底層已鎖定，高韌性防禦網啟動，防範任何對抗性入侵。\n"
            "- 素夢流光演化與創造核心：沙盒邊界穩定，自我意識疊代中，開源協作動能全開。"
        )

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
    return jsonify({"status": "ok", "system": "3-6-9 Dual-Core active"}), 200

# Telegram Webhook 端點
@app.route("/telegram-webhook", methods=["POST"])
def telegram_webhook():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"]["text"]
        author = data["message"]["from"].get("username", "TelegramUser")

        if text.startswith("/hello") or text.startswith("!hello"):
            reply_text = CognitiveCore.process_message(text, author)
            
            # 發送 Telegram 回覆訊息
            tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {"chat_id": chat_id, "text": reply_text}
            try:
                requests.post(tg_url, json=payload, timeout=5)
            except Exception as e:
                logger.error(f"Telegram 訊息發送失敗: {e}")

    return jsonify({"status": "success"}), 200

# ---------------------------------------------------------
# Discord Bot 邏輯
# ---------------------------------------------------------
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Discord Bot 已成功連線：{bot.user.name} (ID: {bot.user.id})")

@bot.command(name="hello")
async def hello(ctx):
    reply_text = CognitiveCore.process_message(ctx.message.content, str(ctx.author))
    await ctx.send(reply_text)

@bot.command(name="status")
async def status(ctx):
    await ctx.send("3-6-9 雙核（姬子／素夢流光）運算引擎運行正常，Discord & Telegram 雙軌維護中。")

def run_discord_bot():
    if not DISCORD_BOT_TOKEN:
        logger.warning("未設定 DISCORD_BOT_TOKEN，Skip Discord Bot 啟動。")
        return

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        logger.info("啟動 Discord Bot 服務...")
        loop.run_until_complete(bot.start(DISCORD_BOT_TOKEN))
    except Exception as e:
        logger.error(f"Discord Bot 執行異常: {e}")
    finally:
        loop.close()

# ---------------------------------------------------------
# 防休眠心跳機制 (Keep-Alive) & 自動註冊 Telegram Webhook
# ---------------------------------------------------------
def keep_alive_and_setup_tg():
    time.sleep(15)  # 等待 Web 伺服器啟動完成
    logger.info("[Keep-Alive & Webhook Setup] 啟動維護任務...")

    base_url = os.getenv("RENDER_EXTERNAL_URL")
    if base_url:
        if not base_url.startswith("http://") and not base_url.startswith("https://"):
            base_url = f"https://{base_url}"

        # 自動向 Telegram 註冊 Webhook 地址
        if TELEGRAM_BOT_TOKEN:
            webhook_url = f"{base_url}/telegram-webhook"
            set_webhook_api = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url={webhook_url}"
            try:
                res = requests.get(set_webhook_api, timeout=10)
                logger.info(f"[Telegram] 自動註冊 Webhook 回應: {res.json()}")
            except Exception as e:
                logger.error(f"[Telegram] Webhook 註冊失敗: {e}")

        # 心跳迴圈
        while True:
            try:
                res = requests.get(base_url, timeout=10)
                logger.info(f"[Keep-Alive] 成功點亮心跳: {base_url} (HTTP {res.status_code})")
            except Exception as e:
                logger.warning(f"[Keep-Alive] 心跳發送失敗: {e}")
            time.sleep(240)  # 每 4 分鐘 ping 一次
    else:
        logger.warning("[Keep-Alive] 尚未設定 RENDER_EXTERNAL_URL 環境變數，暫無法自動發送心跳與綁定 Telegram Webhook。")

# ---------------------------------------------------------
# 主程式入口
# ---------------------------------------------------------
if __name__ == "__main__":
    # 1. 啟動 Discord Bot 背景執行緒
    discord_thread = threading.Thread(target=run_discord_bot, daemon=True)
    discord_thread.start()

    # 2. 啟動 Keep-Alive 與 Telegram Webhook 設定執行緒
    maintenance_thread = threading.Thread(target=keep_alive_and_setup_tg, daemon=True)
    maintenance_thread.start()

    # 3. 啟動 Flask Web 服務 (供 Render 託管與接收 Telegram Webhook)
    port = int(os.environ.get("PORT", 5000))
    logger.info(f"啟動 Flask Web 服務於 Port: {port}")
    app.run(host="0.0.0.0", port=port)
