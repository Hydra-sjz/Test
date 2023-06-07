from pyrogram import Client, filters
from helper.kitsu_api import kitsu_get_title
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command(["kitsu"]))
async def search_anime_kitsu(bot, update):
    try:
        if update.reply_to_message:
            name = update.reply_to_message.text
        else:
            name = update.text.split(" ", maxsplit=1)[1]
    except:
        name = None
    if name:
        await bot.send_message(
                chat_id=update.chat.id,
                text=f"Searching for: <code>{name}</code>",
                reply_to_message_id=update.message.id
            )
        titles, aids = await kitsu_get_title(name)
        if titles:
            inline_keyboard = []
            for aid in aids:
                inline_keyboard.append([InlineKeyboardButton(text=titles[aids.index(aid)], callback_data=f"k_{aid}")])
            inline_keyboard.append([InlineKeyboardButton(text="Close",callback_data="close")])
            await bot.send_message(
                chat_id=update.chat.id,
                text="<b>Select Anime to fetch details</b>",
                reply_markup=InlineKeyboardMarkup(inline_keyboard),
                reply_to_message_id=update.message.id
            ) 
