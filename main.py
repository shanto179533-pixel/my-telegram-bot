import os
import asyncio
from flask import Flask
from threading import Thread
import telebot
from telethon import TelegramClient
from telethon.sessions import StringSession

# Environment variables থেকে ক্রডেনশিয়ালগুলো নেওয়া
API_ID = int(os.getenv("API_ID", "38585154"))
API_HASH = os.getenv("API_HASH", "1e11e2ad0084c11a48df741aabd66a13")
BOT_TOKEN = os.getenv("BOT_TOKEN")
STRING_SESSION = os.getenv("STRING_SESSION")

# Telegram Bot (pyTelegramBotAPI) ইনিশিয়ালাইজ করা
bot = telebot.TeleBot(BOT_TOKEN)

# Telethon Userbot ক্লায়েন্ট তৈরি (Asyncio loop সহ)
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

client = TelegramClient(StringSession(STRING_SESSION), API_ID, API_HASH, loop=loop)
client.start()

# Flask সার্ভার (Render-এর ওয়েব সার্ভিস সচল রাখার জন্য)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    app.run(host='0.0.0.0', port=10000)

# Start কমান্ড হ্যান্ডলার
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 স্বাগতম! ইউজারনেম পাঠান, আমি আইডি বের করে দেব।")

# ইউজারনেম বা মেসেজ হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def get_user_info(message):
    query = message.text.strip()
    
    try:
        # Telethon দিয়ে ইউজারের তথ্য ফেচ করা
        with client:
            entity = client.loop.run_until_complete(client.get_entity(query))
            
            name = getattr(entity, 'first_name', '') or ''
            if getattr(entity, 'last_name', None):
                name += f" {entity.last_name}"
            
            username = f"@{entity.username}" if entity.username else "নেই"
            user_id = entity.id
            
            response = (
                f"✅ **তথ্য পাওয়া গেছে:**\n\n"
                f"👤 **নাম:** {name}\n"
                f"🆔 **আইডি:** `{user_id}`\n"
                f"🔗 **ইউজারনেম:** {username}"
            )
            bot.reply_to(message, response, parse_mode="Markdown")
            
    except Exception as e:
        bot.reply_to(message, "❌ আইডি/ইউজার খুঁজে পাওয়া যায়নি বা এটি পাবলিক নয়!")

# Flask সার্ভার ব্যাকগ্রাউন্ডে রান করা
if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    
    # Bot পোলিং শুরু করা
    bot.infinity_polling()
    
