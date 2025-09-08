import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired, FloodWait
from config import API_ID, API_HASH, BOT_TOKEN, UPDATE_CHANNEL, SOURCE
from datetime import datetime
import asyncio

# Logging config
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# Owner ID
OWNER_ID = 6356050482  # Put your owner ID here

# Bot Client
zeni = Client(
    "zeni",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# START COMMAND
@zeni.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    buttons = [
        [InlineKeyboardButton("Updates", url=UPDATE_CHANNEL)],
        [InlineKeyboardButton("Source", url=SOURCE)]
    ]
    await message.reply_text(
        "🤖 Bot is running successfully!",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

# BAN ALL COMMAND
@zeni.on_message(filters.command("banall"))
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
                await message.reply_text("Need admin rights to ban members")
                break
            except FloodWait as e:
                await asyncio.sleep(e.value)
    except Exception as e:
        print(f"Error banning: {e}")

    await message.reply_text(f"Banned {banned_count} members from {chat_title}")

# LOGS COMMAND
@zeni.on_message(filters.command("logs") & filters.user(OWNER_ID))
async def view_logs_command(client, message):
    try:
        with open("bot.log", "rb") as log_file:
            await message.reply_document(document=log_file, caption="Here are the logs")
    except Exception as e:
        await message.reply_text(f"Error: {e}")

# ALIVE COMMAND
@zeni.on_message(filters.command("alive") & filters.private)
async def alive_command(client, message):
    await message.reply_text("🤖 Bot is alive and working!")

# PING COMMAND
@zeni.on_message(filters.command("ping"))
async def ping_command(client, message):
    start_time = datetime.now()

    await message.reply_text("🏓 Pinging...")
    end_time = datetime.now()

    uptime_seconds = (end_time - start_time).seconds
    uptime_parts = []
    if uptime_seconds > 0:
        uptime_parts.append(f"{uptime_seconds}s")
    formatted_uptime = ' '.join(uptime_parts)

    if message.from_user.id == OWNER_ID:
        response = (
            f"ɪ'ᴍ ᴀʟɪᴠᴇ ᴍʏ ᴍᴀsᴛᴇʀ [✨](https://files.catbox.moe/patnta.mp4)\n\n"
            f"‣ ᴍʏ ᴄʀᴇᴀᴛᴏʀ : [㊝┊𝐙ᴇɴɪᴛꜱᴜ](https://t.me/about_zenuu)\n"
            f"‣ ᴜᴘᴛɪᴍᴇ : {formatted_uptime}\n"
            f"‣ ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ : 𝟸.𝟶.𝟷𝟶𝟼"
        )
    else:
        response = (
            f"ʏᴏᴏ {message.from_user.mention}!\n\n"
            f"‣ ᴜᴘᴛɪᴍᴇ : {formatted_uptime}\n"
            f"‣ ᴍʏ ᴄʀᴇᴀᴛᴏʀ : [㊝┊𝐙ᴇɴɪᴛꜱᴜ](https://t.me/about_zenuu)\n"
            f"‣ ᴘʏʀᴏɢʀᴀᴍ ᴠᴇʀsɪᴏɴ : 𝟸.𝟶.𝟷𝟶𝟼"
        )

    await message.reply_text(response)

# RUN BOT
if __name__ == "__main__":
    zeni.run()
