from pyrogram import *
import requests as re
from mbot import Mbot as app
from pyrogram.types import InlineKeyboardButton,InlineKeyboardMarkup
import wget
import os 
buttons=InlineKeyboardMarkup(
                             [
                             [
            InlineKeyboardButton('Generate', callback_data='generate'),
            InlineKeyboardButton('Refresh', callback_data='refresh'),
            InlineKeyboardButton('Close', callback_data='close')
                   ] 
                             ])
msg_buttons=InlineKeyboardMarkup(
                             [
                             [
            InlineKeyboardButton('View message', callback_data='view_msg'),
            InlineKeyboardButton('Close', callback_data='close')
                   ] 
                             ])
# Fillout The variables in Config.py further queries @riz4d 0n telegram
email=''
@app.on_message(filters.command('tembmail'))
async def start_msgsd(client,message):
    await message.reply("**Hey❕**\n @ is a free service that allows to generates and receive emails at a temporary address that self-destructed after a certain time elapses.\n\n**__ How It Safe's You??**__\n- Using the temporary mail allows you to completely protect your real mailbox against the loss of personal information. Your temporary e-mail address is completely anonymous. Your details: information about your person and users with whom you communicate, IP-address, e-mail address are protected and completely confidential")
    await message.reply("**Generate a Email Now❕**",
                        reply_markup=buttons)
    
    
