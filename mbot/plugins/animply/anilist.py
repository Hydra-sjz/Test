
""" Search for Anime related Info using Anilist API """
import asyncio
from types import NoneType
import requests
import time
import random
import re
import os
from pyrogram import filters, Client
from pyrogram.enums import ChatMemberStatus, ChatType
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputMediaPhoto,
    Message
)
from pyrogram.errors import UserNotParticipant, WebpageCurlFailed, WebpageMediaEmpty
from mbot import (
    ANILIST_CLIENT,
    ANILIST_REDIRECT_URL,
    ANILIST_SECRET,
    OWNER,
    TRIGGERS as trg,
    BOT_NAME,
    Mbot as anibot
)
from mbot.utils2.data_parser import (
    get_all_genres,
    get_all_tags,
    get_studio_animes,
    get_studios,
    get_top_animes,
    get_user_activity,
    get_user_favourites,
    toggle_favourites,
    get_anime,
    get_airing,
    get_anilist,
    get_character,
    get_additional_info,
    get_manga,
    browse_,
    get_featured_in_lists,
    update_anilist,
    get_user,
    ANIME_DB,
    MANGA_DB,
    CHAR_DB,
    AIRING_DB,
    STUDIO_DB,
    GUI
)
from mbot.utils2.helper import (
    clog,
    check_user,
    get_btns,
    rand_key,
    control_user,
    get_user_from_channel as gcc,
    PIC_LS,
    AUTH_USERS
)
from mbot.utils2.db import get_collection
GROUPS = get_collection("GROUPS")
SFW_GRPS = get_collection("SFW_GROUPS")
DC = get_collection('DISABLED_CMDS')
AG = get_collection('AIRING_GROUPS')
CG = get_collection('CRUNCHY_GROUPS')
SG = get_collection('SUBSPLEASE_GROUPS')
HD = get_collection('HEADLINES_GROUPS')
MHD = get_collection('MAL_HEADLINES_GROUPS')
CHAT_OWNER = ChatMemberStatus.OWNER
MEMBER = ChatMemberStatus.MEMBER
ADMINISTRATOR = ChatMemberStatus.ADMINISTRATOR
failed_pic = "https://telegra.ph/file/09733b49f3a9d5b147d21.png"
no_pic = [
    'https://telegra.ph/file/0d2097f442e816ba3f946.jpg',
    'https://telegra.ph/file/5a152016056308ef63226.jpg',
    'https://telegra.ph/file/d2bf913b18688c59828e9.jpg',
    'https://telegra.ph/file/d53083ea69e84e3b54735.jpg',
    'https://telegra.ph/file/b5eb1e3606b7d2f1b491f.jpg'
]


@anibot.on_message(
    filters.command(["anime", f"anime{BOT_NAME}"], prefixes=trg)
)
@control_user
async def anime_cmd(client: Client, message: Message, mdata: dict):
    """Search Anime Info"""
    text = mdata['text'].split(" ", 1)
    gid = mdata['chat']['id']
    try:
        user = mdata['from_user']['id']
        auser = mdata['from_user']['id']
    except KeyError:
        user = mdata['sender_chat']['id']
        ufc = await gcc(user)
        if ufc is not None:
            auser = ufc
        else:
            auser = user
    find_gc = await DC.find_one({'_id': gid})
    if find_gc is not None and 'anime' in find_gc['cmd_list'].split():
        return
    if len(text) == 1:
        k = await message.reply_text(
"""Please give a query to search about
example: /anime Ao Haru Ride"""
        )
        await asyncio.sleep(5)
        return await k.delete()
    query = text[1]
    auth = False
    vars_ = {"search": query}
    if query.isdigit():
        vars_ = {"id": int(query)}
    if (await AUTH_USERS.find_one({"id": auser})):
        auth = True
    result = await get_anime(
        vars_,
        user=auser,
        auth=auth,
        cid=gid if gid != user else None
    )
    if len(result) != 1:
        title_img, finals_ = result[0], result[1]
    else:
        k = await message.reply_text(result[0])
        await asyncio.sleep(5)
        return await k.delete()
    buttons = get_btns("ANIME", result=result, user=user, auth=auth)
    if await (
        SFW_GRPS.find_one({"id": gid})
    ) and result[2].pop() == "True":
        await client.send_photo(
            gid,
            no_pic[random.randint(0, 4)],
            caption="This anime is marked 18+ and not allowed in this group"
        )
        return
    try:
        await client.send_photo(
            gid, title_img, caption=finals_, reply_markup=buttons
        )
    except (WebpageMediaEmpty, WebpageCurlFailed):
        await clog('ANIBOT', title_img, 'LINK', msg=message)
        await client.send_photo(
            gid, failed_pic, caption=finals_, reply_markup=buttons
        )
    if title_img not in PIC_LS:
        PIC_LS.append(title_img)
@anibot.on_message(
    filters.command(["manga", f"manga{BOT_NAME}"], prefixes=trg)
)
@control_user
async def manga_cmd(client: Client, message: Message, mdata: dict):
    """Search Manga Info"""
    text = mdata['text'].split(" ", 1)
    gid = mdata['chat']['id']
    try:
        user = mdata['from_user']['id']
        auser = mdata['from_user']['id']
    except KeyError:
        user = mdata['sender_chat']['id']
        ufc = await gcc(user)
        if ufc is not None:
            auser = ufc
        else:
            auser = user
    find_gc = await DC.find_one({'_id': gid})
    if find_gc is not None and 'manga' in find_gc['cmd_list'].split():
        return
    if len(text) == 1:
        k = await message.reply_text(
"""Please give a query to search about
example: /manga The teasing master Takagi san"""
        )
        await asyncio.sleep(5)
        return await k.delete()
    query = text[1]
    qdb = rand_key()
    MANGA_DB[qdb] = query
    auth = False
    if (await AUTH_USERS.find_one({"id": auser})):
        auth = True
    result = await get_manga(
        qdb, 1, auth=auth, user=auser, cid=gid if gid != user else None
    )
    if len(result) == 1:
        k = await message.reply_text(result[0])
        await asyncio.sleep(5)
        return await k.delete()
    pic, finals_ = result[0], result[1][0]
    buttons = get_btns(
        "MANGA",
        lsqry=qdb,
        lspage=1,
        user=user,
        result=result,
        auth=auth
    )
    if await (SFW_GRPS.find_one({"id": gid})) and result[2].pop() == "True":
        buttons = get_btns(
            "MANGA",
            lsqry=qdb,
            lspage=1,
            user=user,
            result=result,
            auth=auth,
            sfw="True"
        )
        await client.send_photo(
            gid,
            no_pic[random.randint(0, 4)],
            caption="This manga is marked 18+ and not allowed in this group",
            reply_markup=buttons
        )
        return
    try:
        await client.send_photo(
            gid, pic, caption=finals_, reply_markup=buttons
        )
    except (WebpageMediaEmpty, WebpageCurlFailed):
        await clog('ANIBOT', pic, 'LINK', msg=message)
        await client.send_photo(
            gid, failed_pic, caption=finals_, reply_markup=buttons
        )
    if pic not in PIC_LS:
        PIC_LS.append(pic)
