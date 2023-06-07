from pyrogram import *
import requests as re
from mbot import Mbot as app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import wget
import os 
import requests
from pyrogram import filters, Client
from helper.kitsu_api import kitsu_get_anime


email=''


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


@app.on_callback_query()
async def mailbox(client,message):
    response=message.data
    if response=='generate':
       global email
       email = re.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1").json()[0]
       await message.edit_message_text('__**Your Temporary E-mail: **__`'+str(email)+'`',
                                       reply_markup=buttons)
       print(email)
    elif response=='refresh':
        print(email)
        try:
            if email=='':
                await message.edit_message_text('Genaerate a email',reply_markup=buttons)
            else: 
                getmsg_endp =  "https://www.1secmail.com/api/v1/?action=getMessages&login=" + email[:email.find("@")] + "&domain=" + email[email.find("@") + 1:]
                print(getmsg_endp)
                ref_response = re.get(getmsg_endp).json()
                global idnum
                idnum=str(ref_response[0]['id'])
                from_msg=ref_response[0]['from']
                subject=ref_response[0]['subject']
                refreshrply='You a message from '+from_msg+'\n\nSubject : '+subject
                await message.edit_message_text(refreshrply,
                                                reply_markup=msg_buttons)
        except:
            await message.answer('No messages were received..\nin your Mailbox '+email)
    elif response=='view_msg':
        msg =re.get("https://www.1secmail.com/api/v1/?action=readMessage&login=" + email[:email.find("@")] + "&domain=" + email[email.find("@") + 1:] + "&id=" + idnum).json()
        print(msg)
        from_mail=msg['from']
        date=msg['date']
        subjectt=msg['subject']
        try:
          attachments=msg['attachments'][0]
        except:
            pass
        body=msg['body']
        mailbox_view='ID No : '+idnum+'\nFrom : '+from_mail+'\nDate : '+date+'\nSubject : '+subjectt+'\nmessage : \n'+body
        await message.edit_message_text(mailbox_view,reply_markup=buttons)
        mailbox_view='ID No : '+idnum+'\nFrom : '+from_mail+'\nDate : '+date+'\nSubject : '+subjectt+'\nmessage : \n'+body
        if attachments == "[]":
            await message.edit_message_text(mailbox_view,reply_markup=buttons)
            await message.answer("No Messages Were Recieved..", show_alert=True)
        else:
            dlattach=attachments['filename']
            attc="https://www.1secmail.com/api/v1/?action=download&login=" + email[:email.find("@")] + "&domain=" + email[email.find("@") + 1:] + "&id=" + idnum+"&file="+dlattach
            print(attc)
            mailbox_vieww='ID No : '+idnum+'\nFrom : '+from_mail+'\nDate : '+date+'\nSubject : '+subjectt+'\nmessage : \n'+body+'\n\n'+'[Download]('+attc+') Attachments'
            filedl=wget.download(attc)
            await message.edit_message_text(mailbox_vieww,reply_markup=buttons)
            os.remove(dlattach)
            
#UD
@app.on_callback_query(filters.regex("^udnxt"))   
async def next(_, query):
         user_id = int(query.data.split(":")[1])
         text = str(query.data.split(":")[2])
         num = int(query.data.split(":")[3])+1
         if not query.from_user.id == user_id:
             return await query.answer("This is not for You!")
         api = requests.get(f"https://api.urbandictionary.com/v0/define?term={text}").json()
         mm = api["list"]
         uwu = mm[num]
         if num == len(mm)-1:
             string = f"🔍 **Ward**: {uwu.get('word')}\n\n📝 **Definition**: {uwu.get('definition')}\n\n✏️ **Example**: {uwu.get('example')}\n\n"
             string += f"Page: {num+1}/{len(mm)}"
             return await query.message.edit(text=string, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('➡️ Back', callback_data=f"udbck:{query.from_user.id}:{text}:{num}")]]))
         else:
             string = f"🔍 **Ward**: {uwu.get('word')}\n\n📝 **Definition**: {uwu.get('definition')}\n\n✏️ **Example**: {uwu.get('example')}\n\n"
             string += f"Page: {num+1}/{len(mm)}"
             buttons = [[
                  InlineKeyboardButton("⬅️", callback_data=f"udbck:{query.from_user.id}:{text}:{num}"),
                  InlineKeyboardButton("➡️", callback_data=f"udnxt:{query.from_user.id}:{text}:{num}") 
             ]]
             return await query.message.edit(text=string, reply_markup=InlineKeyboardMarkup(buttons))
@app.on_callback_query(filters.regex("^udbck"))   
async def back(_, query):
         user_id = int(query.data.split(":")[1])
         text = str(query.data.split(":")[2])
         num = int(query.data.split(":")[3])-1
         if not query.from_user.id == user_id:
             return await query.answer("This is not for You!")
         api = requests.get(f"https://api.urbandictionary.com/v0/define?term={text}").json()
         mm = api["list"]
         uwu = mm[num]
         if num == 0:
             string = f"🔍 **Ward**: {uwu.get('word')}\n\n📝 **Definition**: {uwu.get('definition')}\n\n✏️ **Example**: {uwu.get('example')}\n\n"
             string += f"Page: {num+1}/{len(mm)}"
             return await query.message.edit(text=string, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('➡️ Next', callback_data=f"udnxt:{query.from_user.id}:{text}:{num}")]]))
         else:
             string = f"🔍 **Ward**: {uwu.get('word')}\n\n📝 **Definition**: {uwu.get('definition')}\n\n✏️ **Example**: {uwu.get('example')}\n\n"
             string += f"Page: {num+1}/{len(mm)}"
             buttons = [[
                  InlineKeyboardButton("⬅️", callback_data=f"udbck:{query.from_user.id}:{text}:{num}"),
                  InlineKeyboardButton("➡️", callback_data=f"udnxt:{query.from_user.id}:{text}:{num}") 
             ]]
             return await query.message.edit(text=string, reply_markup=InlineKeyboardMarkup(buttons))
            
@app.on_callback_query(filters.regex("k_"))
async def get_anime_kitsu_cb(c: Client, cb: CallbackQuery):
    a_id = cb.data.split("_")[1]
    photo, msg = await kitsu_get_anime(a_id)
    if msg:
        await c.delete_messages(chat_id=cb.message.chat.id, message_ids=[cb.message.id])
        await c.send_photo(
            chat_id=cb.message.chat.id,
            photo=photo,
            caption=msg,
            reply_to_message_id=cb.message.reply_to_message.message.id
        ) 
      
            
            
            
            
            
            
