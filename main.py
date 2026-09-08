from telethon.tl.functions.contacts import ResolveUsernameRequest

# ইউজারনেম বা মেসেজ হ্যান্ডলারের ভেতরে try ব্লকের মধ্যে এভাবে দিন:
with client:
    username = query.replace('@', '').strip()
    result = client.loop.run_until_complete(
        client(ResolveUsernameRequest(username))
    )
    
    # এর পর ইউজার বা চ্যানেলের অবজেক্ট পেয়ে যাবেন
    entity = result.users[0] if result.users else result.chats[0]
    
    name = getattr(entity, 'first_name', '') or getattr(entity, 'title', '')
    user_id = entity.id
    
    response = (
        f"✅ **তথ্য পাওয়া গেছে:**\n\n"
        f"👤 **নাম:** {name}\n"
        f"🆔 **আইডি:** `{user_id}`\n"
        f"🔗 **ইউজারনেম:** @{username}"
    )
    bot.reply_to(message, response, parse_mode="Markdown")
    
