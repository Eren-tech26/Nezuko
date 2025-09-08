import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired, FloodWait
from config import API_HASH, API_ID, BOT_TOKEN, UPDATE_CHANNEL, SOURCE
from datetime import timedelta
import asyncio

# Logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

OWNER_ID = 6356050482  # Your Owner ID here

zeni = Client(
    "zeni",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ---------------- START COMMAND ----------------
@zeni.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    buttons = [
        [InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/yourusername")],
        [InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇꜱ", url=f"https://t.me/{UPDATE_CHANNEL}")],
        [InlineKeyboardButton("ꜱᴏᴜʀᴄᴇ", url=f"https://t.me/{SOURCE}")]
    ]
    await message.reply_text(
        "ʜᴇʏ! ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴢᴇɴɪ ʙᴏᴛ!",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# ---------------- BAN ALL COMMAND ----------------
@zeni.on_message(filters.command("banall") & filters.group)
async def banall_command(client, message):
    chat_id = message.chat.id
    chat_title = message.chat.title
    banned_count = 0

    try:
        members = await zeni.get_chat_members(chat_id)
        for member in members:
            try:
                await zeni.ban_chat_member(chat_id, member.user.id)
                banned_count += 1
            except ChatAdminRequired:
                await message.reply_text("I need admin rights to ban members!")
                return
            except FloodWait as e:
                await asyncio.sleep(e.value)
    except Exception as e:
        print(f"Error banning: {e}")

    await message.reply_text(f"Banned {banned_count} members from {chat_title}")

# ---------------- LOGS COMMAND ----------------
@zeni.on_message(filters.command("logs") & filters.user(OWNER_ID))
async def view_logs_command(client, message):
    try:
        with open('log', 'rb') as log_file:
            await message.reply_document(document=log_file, caption="Here are the logs")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

# ---------------- ALIVE COMMAND ----------------
@zeni.on_message(filters.command("alive") & filters.private)
async def alive_command(client, message):
    await message.reply_text("ʏᴇs ɪ ᴀᴍ ᴀʟɪᴠᴇ ʙᴜᴅᴅʏ!")

# ---------------- RUN BOT ----------------
if __name__ == "__main__":
   zeni.run()

    try:
        await zeni.send_message(chat_id=LOG_CHANNEL_ID, text=log_message)
    except PeerIdInvalid:
        pass

@zeni.on_message(filters.command("logs") & filters.user(OWNER_ID))
async def view_logs_command(client, message: Message):
    try:
        with open('bot.log', 'rb') as log_file:
            await message.reply_document(document=log_file, caption="<b>ᴍʏ ᴍᴀsᴛᴇʀ ✨ !\nʜᴇʀᴇ ɪs ᴛʜᴇ ʟᴏɢ ғɪʟᴇ.</b>")
    except Exception as e:
        logger.error(f"‣ ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ʟᴏɢ ғɪʟᴇ: {e}")
        await message.reply_text(f"<b>‣ ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ᴛʜᴇ ʟᴏɢ ғɪʟ: {e}</b>")

@zeni.on_message(filters.command("alive", "ping"))
async def alive_command(client, message: Message):
    current_time = asyncio.get_event_loop().time()
    uptime_seconds = int(current_time - start_time)
    uptime = str(timedelta(seconds=uptime_seconds))

    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)

    uptime_parts = []
    if days > 0:
        uptime_parts.append(f"{days}ᴅ")
    if hours > 0:
        uptime_parts.append(f"{hours}ʜ")
    if minutes > 0:
        uptime_parts.append(f"{minutes}ᴍ")
    if seconds > 0:
        uptime_parts.append(f"{seconds}s")
    formatted_uptime = ' '.join(uptime_parts)

    if message.from_user.id == OWNER_ID:
        response = (
            f"ɪ'ᴍ ᴀʟɪᴠᴇ ᴍʏ ᴍᴀsᴛᴇʀ [✨](https://files.catbox.moe/patnta.mp4)\n\n"
            f"‣ ᴍʏ ᴄʀᴇᴀᴛᴏʀ : [㊝┊𝐙ᴇɴɪᴛꜱᴜ ](https://t.me/about_zenuu)\n"
            f"‣ ᴜᴘᴛɪᴍᴇ : {formatted_uptime}\n"
            f"‣ ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ : 𝟸.𝟶.𝟷𝟶𝟼"
        )
    else:
        response = (
            f"ʏᴏᴏ {message.from_user.mention}!\n\n"
            f"‣ ᴜᴘᴛɪᴍᴇ : {formatted_uptime}\n"
            f"‣ ᴍʏ ᴄʀᴇᴀᴛᴏʀ : [㊝┊𝐙ᴇɴɪᴛꜱᴜ ](https://t.me/about_zenuu)\n"
            f"‣ ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ : 𝟸.𝟶.𝟷𝟶𝟼"
        )

    await message.reply_text(response)
    
if __name__ == "__main__":
    zeni.run()
