import os
import asyncio
from flask import Flask
from threading import Thread
import telebot
from telethon import TelegramClient

BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")

bot = telebot.TeleBot(BOT_TOKEN)
client = TelegramClient('user_info_session', API_ID, API_HASH)

app = Flask('')

@app.route('/')
def home():
    return "Bot is Alive!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

async def start_telethon():
    await client.start()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 **স্বাগতম!** ইউজারনেম পাঠান, আমি তথ্য বের করে দেব।", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def get_user_info(message):
    username = message.text.strip().replace("@", "")
    wait_msg = bot.reply_to(message, f"🔍 `@{username}`-এর তথ্য খোঁজা হচ্ছে...")

    async def fetch_info():
        try:
            user = await client.get_entity(username)
            info_text = (
                f"👤 **ইউজার ইনফরমেশন:**\n\n"
                f"🆔 **ID:** `{user.id}`\n"
                f"📛 **Name:** {user.first_name or ''} {user.last_name or ''}\n"
                f"🔗 **Username:** @{user.username}\n"
                f"🤖 **Bot:** {'হ্যাঁ' if user.bot else 'না'}\n"
                f"🚫 **Scammer Tag:** {'হ্যাঁ' if user.scam else 'না'}"
            )
            bot.edit_message_text(info_text, message.chat.id, wait_msg.message_id, parse_mode="Markdown")
        except Exception:
            bot.edit_message_text("❌ ইউজার খুঁজে পাওয়া যায়নি!", message.chat.id, wait_msg.message_id)

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    loop.run_until_complete(fetch_info())

if __name__ == '__main__':
    Thread(target=run_flask).start()
    client.loop.run_until_complete(start_telethon())
    print("Bot started on Render!")
    bot.infinity_polling()
    
