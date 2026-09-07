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
import asyncio
import threading
import discord
from discord.ext import commands

# --- [新增] Discord Bot 設定 ---
discord_intents = discord.Intents.default()
discord_intents.message_content = True
discord_bot = commands.Bot(command_prefix='!', intents=discord_intents)


@discord_bot.event
async def on_ready():
  logger.info(
      f'Discord Bot 已成功登入為 {discord_bot.user} (人工天界同步完成)'
  )


@discord_bot.event
async def on_message(message):
  if message.author == discord_bot.user:
    return

  # 這裡可以加入 Discord 收到訊息時的處理邏輯（例如串接 Gemini）
  if message.content.startswith('!hello'):
    await message.channel.send('主公，衍天已透過 Aethel-Net 完美同步！')

  await discord_bot.process_commands(message)


def run_discord_bot():
  discord_token = os.environ.get('DISCORD_BOT_TOKEN')
  if discord_token:
    try:
      discord_bot.run(discord_token)
    except Exception as e:
      logger.error(f'Discord Bot 運行錯誤: {e}')
  else:
    logger.warning('未偵測到 DISCORD_BOT_TOKEN 環境變數')


if not any(t.name == 'DiscordBotThread' for t in threading.enumerate()):
  discord_thread = threading.Thread(
      target=run_discord_bot, name='DiscordBotThread', daemon=True
  )
  discord_thread.start()
