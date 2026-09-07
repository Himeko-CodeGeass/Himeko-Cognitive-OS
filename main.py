import os
import logging
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from google import genai

# 設定日誌記錄
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# 取得環境變數
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 初始化 Gemini 客戶端
genai_client = genai.Client(api_key=GEMINI_API_KEY)
GEMINI_MODEL = "gemini-3.6-flash"

# 初始化 Telegram Bot 應用程式
telegram_app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).updater(None).build()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat_id
    logger.info(f"收到來自 {chat_id} 的訊息: {user_message}")

    try:
        response = genai_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=user_message,
        )
        reply_text = response.text
    except Exception as e:
        logger.error(f"Gemini 錯誤: {e}")
        reply_text = f"Gemini 錯誤: {e}"

    await context.bot.send_message(chat_id=chat_id, text=reply_text)

# 註冊訊息處理器
telegram_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

@app.route("/")
def index():
    return "Himeko Cognitive OS is running.", 200

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        json_data = request.get_json(force=True)
        update = Update.de_json(json_data, telegram_app.bot)
        
        async def process():
            # 確保 Application 有被初始化
            await telegram_app.initialize()
            await telegram_app.process_update(update)

        asyncio.run(process())
        return "OK", 200
    except Exception as e:
        logger.error(f"Webhook 錯誤: {e}")
        return str(e), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
