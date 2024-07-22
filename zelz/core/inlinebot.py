import json
import math
import asyncio
import os
import random
import re
import time
from pathlib import Path
from uuid import uuid4
from platform import python_version
from telethon import Button, types, version
from telethon.errors import QueryIdInvalidError
from telethon.events import CallbackQuery, InlineQuery
from telethon.tl.functions.users import GetUsersRequest
from youtubesearchpython import VideosSearch
from zelz import zedub, zedversion, StartTime
from ..Config import Config
from ..helpers import reply_id
from ..helpers.utils import _format
from ..helpers.functions import rand_key, zedalive, check_data_base_heal_th, get_readable_time
from ..helpers.functions.utube import download_button, get_yt_video_id, get_ytthumb, result_formatter, ytsearch_data
from ..plugins import mention
from ..sql_helper.globals import gvarstatus
from . import CMD_INFO, GRP_INFO, PLG_INFO, check_owner, mention
from .logger import logging

LOGS = logging.getLogger(__name__)

BTN_URL_REGEX = re.compile(r"(\[([^\[]+?)\]\<buttonurl:(?:/{0,2})(.+?)(:same)?\>)")
MEDIA_PATH_REGEX = re.compile(r"(:?\<\bmedia:(:?(?:.*?)+)\>)")
tr = Config.COMMAND_HAND_LER

scc = "secret"
hmm = "همسـة"
ymm = "يستطيـع"
fmm = "فتـح الهمسـه 🗳"
dss = "⌔╎هو فقط من يستطيع ࢪؤيتهـا"
hss = "[ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - همسـة سـࢪيـه 📠](t.me/ZThon)\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n**⌔╎الهمسـة لـ**"
nmm = "همسـه سريـه"
mnn = "ارسـال همسـه سريـه لـ (شخـص/اشخـاص).\nعبـر زدثــون"
bmm = "اضغـط للـرد"
ttt = "ᯓ 𝗦𝗢𝗨𝗥𝗖𝗘 𝗭𝗧𝗛𝗢𝗡 - همسـة سـࢪيـه\n⋆┄─┄─┄─┄┄─┄─┄─┄─┄┄⋆\n\n⌔╎اضغـط الـزر 🚹\n⌔╎لـ اࢪسـال همسـه سـࢪيـه الى"
ddd = "💌\n⌔╎او اضغـط الـزر 🛗\n⌔╎لـ اࢪسـال همسـه جماعية الى نفـس الشخص وأشخـاص آخرون📨"
bbb = None

def getkey(val):
    for key, value in GRP_INFO.items():
        for plugin in value:
            if val == plugin:
                return key
    return None

def get_thumb(name):
    url = f"https://github.com/TgCatUB/CatUserbot-Resources/blob/master/Resources/Inline/{name}?raw=true"
    return types.InputWebDocument(url=url, size=0, mime_type="image/png", attributes=[])

def ibuild_keyboard(buttons):
    keyb = []
    for btn in buttons:
        if btn[2] and keyb:
            keyb[-1].append(Button.url(btn[0], btn[1]))
        else:
            keyb.append([Button.url(btn[0], btn[1])])
    return keyb

@zedub.tgbot.on(InlineQuery)
async def inline_handler(event):  # sourcery no-metrics
    builder = event.builder
    result = None
    query = event.text
    string = query.lower()
    query.split(" ", 2)
    str_y = query.split(" ", 1)
    string.split()
    query_user_id = event.query.user_id
    user_id = gvarstatus("hmsa_id")
    full_name = gvarstatus("hmsa_name")
    username = gvarstatus("hmsa_user")
    if username.startswith("@"):
        zelzal = gvarstatus("hmsa_user")
    else:
        zelzal = f"[{full_name}](tg://user?id={user_id})"
    if query_user_id == Config.OWNER_ID or query_user_id in Config.SUDO_USERS:  # Code by T.me/zzzzl1l
        malathid = Config.OWNER_ID
    elif query_user_id == user_id or query_user_id == int(user_id):
        malathid = user_id
    else:
        malathid = None
    if query_user_id == Config.OWNER_ID or query_user_id == user_id or query_user_id in Config.SUDO_USERS:  # Code by T.me/zzzzl1l
        inf = re.compile("secret (.*) (.*)")
        match2 = re.findall(inf, query)
        if match2:
            user_list = []
            zilzal = ""
            query = query[7:]
            info_type = [hmm, ymm, fmm]
            if "|" in query:
                iris, query = query.replace(" |", "|").replace("| ", "|").split("|")
                users = iris.split(" ")
            else:
                user, query = query.split(" ", 1)
                users = [user]
            for user in users:
                usr = int(user) if user.isdigit() else user
                try:
                    u = await zedub.get_entity(usr)
                except ValueError:
                    u = await zedub(GetUsersRequest(usr))
                if u.username:
                    zilzal += f"@{u.username}"
                else:
                    zilzal += f"[{u.first_name}](tg://user?id={u.id})"
                user_list.append(u.id)
                zilzal += " "
            zilzal = zilzal[:-1]
            old_msg = os.path.join("./zelz", f"{user_id}.txt")
            try:
                jsondata = json.load(open(old_msg))
            except Exception:
                jsondata = False
            timestamp = int(time.time() * 2)
            new_msg = {
                str(timestamp): {"userid": user_list, "text": query}
            }  # Code by T.me/zzzzl1l
            buttons = [[Button.inline(info_type[2], data=f"{scc}_{timestamp}")],[Button.switch_inline(bmm, query=f"secret {malathid} \nهلو", same_peer=True)]]
            result = builder.article(
                title=f"{hmm} {zilzal}",
                description=f"{dss}",
                text=f"{hss} {zilzal} \n**{dss}**",
                buttons=buttons,
                link_preview=False,
            )
            await event.answer([result] if result else None)
            if jsondata:
                jsondata.update(new_msg)
                json.dump(jsondata, open(old_msg, "w"))
            else:
                json.dump(new_msg, open(old_msg, "w"))
        elif string == "zelzal":
            if gvarstatus("hmsa_id"):
                bbb = [(Button.switch_inline("🛗", query=("secret " + gvarstatus("hmsa_id") + " @يوزر2 | \nهلو"), same_peer=True), Button.switch_inline("🚹", query=("secret " + gvarstatus("hmsa_id") + " \nهلو"), same_peer=True))]
            else:
                return
            results = []
            results.append(
                builder.article(
                    title=f"{nmm}",
                    description=f"{mnn}",
                    text=f"**{ttt}** {zelzal} **{ddd}**",
                    buttons=bbb,
                    link_preview=False,
                ),
            )
            return await event.answer(results)
        elif str_y[0].lower() == "ytdl" and len(str_y) == 2:
            link = get_yt_video_id(str_y[1].strip())
            found_ = True
            if link is None:
                search = VideosSearch(str_y[1].strip(), limit=15)
                resp = (search.result()).get("result")
                if len(resp) == 0:
                    found_ = False
                else:
                    outdata = await result_formatter(resp)
                    key_ = rand_key()
                    ytsearch_data.store_(key_, outdata)
                    buttons = [
                        Button.inline(
                            f"1 / {len(outdata)}",
                            data=f"ytdl_next_{key_}_1",
                        ),
                        Button.inline(
                            "القائمـة 📜",
                            data=f"ytdl_listall_{key_}_1",
                        ),
                        Button.inline(
                            "⬇️  تحميـل",
                            data=f'ytdl_download_{outdata[1]["video_id"]}_0',
                        ),
                    ]
                    caption = outdata[1]["message"]
                    photo = await get_ytthumb(outdata[1]["video_id"])
            else:
                caption, buttons = await download_button(link, body=True)
                photo = await get_ytthumb(link)
            if found_:
                markup = event.client.build_reply_markup(buttons)
                photo = types.InputWebDocument(
                    url=photo, size=0, mime_type="image/jpeg", attributes=[]
                )
                text, msg_entities = await event.client._parse_message_text(
                    caption, "html"
                )
                result = types.InputBotInlineResult(
                    id=str(uuid4()),
                    type="photo",
                    title=link,
                    description="⬇️ اضغـط للتحميـل",
                    thumb=photo,
                    content=photo,
                    send_message=types.InputBotInlineMessageMediaAuto(
                        reply_markup=markup, message=text, entities=msg_entities
                    ),
                )
            else:
                result = builder.article(
                    title="Not Found",
                    text=f"No Results found for `{str_y[1]}`",
                    description="INVALID",
                )
            try:
                await event.answer([result] if result else None)
            except QueryIdInvalidError:
                await event.answer(
                    [
                        builder.article(
                            title="Not Found",
                            text=f"No Results found for `{str_y[1]}`",
                            description="INVALID",
                        )
                    ]
                )
        elif string == "pmpermit":
            controlpmch = gvarstatus("pmchannel") or None
            if controlpmch is not None:
                zchannel = controlpmch.replace("@", "")
                buttons = [[Button.url("⌔ قنـاتـي ⌔", f"https://t.me/{zchannel}")]]
            else:
                buttons = [[Button.url("𝗭𝗧𝗵𝗼𝗻", "https://t.me/ZThon")]]
            PM_PIC = gvarstatus("pmpermit_pic")
            if PM_PIC:
                CAT = [x for x in PM_PIC.split()]
                PIC = list(CAT)
                CAT_IMG = random.choice(PIC)
            else:
                CAT_IMG = None
            query = gvarstatus("pmpermit_text")
            if CAT_IMG and CAT_IMG.endswith((".jpg", ".jpeg", ".png")):
                result = builder.photo(
                    CAT_IMG,
                    # title="Alive zed",
                    text=query,
                    buttons=buttons,
                )
            elif CAT_IMG:
                result = builder.document(
                    CAT_IMG,
                    title="Alive cat",
                    text=query,
                    buttons=buttons,
                )
            else:
                result = builder.article(
                    title="Alive cat",
                    text=query,
                    buttons=buttons,
                )
            await event.answer([result] if result else None)
