from pyrogram import filters
from mbot import Mbot




@Mbot.on_message(filters.private & filters.command("start"))
async def start_command(bot, message):
    await message.reply_text("hello fucker")
