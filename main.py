import os
from flask import Flask
from threading import Thread
import telebot

BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot is Alive!"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 **স্বাগতম!** ইউজারনেম পাঠান, আমি আইডি বের করে দেব।", parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def get_user_info(message):
    username = message.text.strip().replace("@", "")
    wait_msg = bot.reply_to(message, f"🔍 `@{username}`-এর তথ্য খোঁজা হচ্ছে...")

    try:
        chat = bot.get_chat(f"@{username}")
        info_text = (
            f"👤 **ইউজার/চ্যাট ইনফরমেশন:**\n\n"
            f"🆔 **ID:** `{chat.id}`\n"
            f"📛 **Title/Name:** {chat.first_name or ''} {chat.last_name or ''} {chat.title or ''}\n"
            f"🔗 **Username:** @{chat.username}\n"
            f"📝 **Type:** {chat.type}\n"
            f"📌 **Bio:** {chat.bio or 'N/A'}"
        )
        bot.edit_message_text(info_text, message.chat.id, wait_msg.message_id, parse_mode="Markdown")
    except Exception:
        bot.edit_message_text("❌ আইডি/ইউজার খুঁজে পাওয়া যায়নি বা এটি পাবলিক নয়!", message.chat.id, wait_msg.message_id)

if __name__ == '__main__':
    Thread(target=run_flask).start()
    print("Bot started on Render!")
    bot.infinity_polling()
    
