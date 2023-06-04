import re
import random
import asyncio
from TheHanCock.helpers.utils import get_shortlink
from config import AUTH_CHANNEL, AUTH_USERS, CUSTOM_FILE_CAPTION, API_KEY, AUTH_GROUPS, BUTTON
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters, enums
from pyrogram.errors import UserNotParticipant
from TheHanCock.helpers.utils import get_filter_results, get_file_details, is_subscribed, get_poster
from config import PREMIUMS as subscriptions

BUTTONS = {}
BOT = {}

# ------------------» ᴛᴇxᴛ-sʏɴᴛᴀx «------------------ #

PLANS_IMG = "https://telegra.ph/file/53b043a4674e3613d2380.jpg"

PLANS_TEXT = """<code>
ɪғ ʏᴏᴜ ʙᴜʏ ᴘʟᴀɴ ᴛʜᴇɴ ʏᴏᴜ ɢᴇᴛ ᴅɪʀᴇᴄᴛ ᴍᴏᴠɪᴇs ғɪʟᴇ 

ᴇɴᴊᴏʏ ʏᴏᴜʀ ᴘʟᴀɴ ᴀɴᴅ ɢᴇᴛ ᴍᴏʀᴇ ᴍᴏᴠɪᴇs ᴡɪᴛʜ ᴀᴅᴅ ғʀᴇᴇ

ᴛʜᴇsᴇ ᴀʀᴇ ᴀʟʟ ᴛʜᴇ ᴘʟᴀɴs ᴀᴠᴀɪʟᴀʙʟᴇ !

ᴋɪɴᴅʟʏ ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ᴛᴏ ᴀᴄᴛɪᴠᴀᴛᴇ ᴏɴᴇ.</code>
[ᴄʟɪᴄᴋ](https://t.me/Reqstmovies)
"""

HOW_TO_PAY = """
<u>ʜᴏᴡ ᴛᴏ ᴘᴀʏ ᴍᴏɴᴇʏ</u>
<code>» sᴛᴇᴘ 𝟷 : sᴄᴀɴ ʙᴀʀ ᴄᴏᴅᴇ ᴏʀ ᴘᴀʏ ᴏɴ ᴛʜɪs ᴜᴘɪ</code> : <code> reqstmovies@ybl </code>

<code>» sᴛᴇᴘ 𝟸 : ᴄʟɪᴄᴋ ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ ʙᴜᴛᴛᴏɴ ᴀɴᴅ sᴇɴᴅ ᴘᴀʏᴍᴇɴᴛ sᴄʀᴇᴇɴsʜᴏᴛ.</code>

<code>» sᴛᴇᴘ 𝟹 : ɪ ᴡɪʟʟ ᴀᴅᴅ ʏᴏᴜʀ ᴘʟᴀɴ ɪɴsᴛᴀɴᴛ.</code>
"""

# ------------------» ᴛᴇxᴛ-sʏɴᴛᴀx «------------------ #


@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        sumit=BOT.get("username")    
        if not sumit:
            botusername=await client.get_me()
            sumit=botusername.username
            BOT["username"]=sumit
        files = await get_filter_results(query=search)
    if message.from_user.id in subscriptions:
        if files:
            btn.append(
                    [
                        InlineKeyboardButton("✅ ʜᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ✅", url=f"https://t.me/TheMoviesUpdate/130")
                    ]
                    )
            btn.append(
                    [                                       
                        InlineKeyboardButton("⊙ ᴅɪʀᴇᴄᴛ ғɪʟᴇ|ᴄʟɪᴄᴋ ʜᴇʀᴇ ⊙", callback_data="Direct_file")
                    ] 
                    ) 
    
            for file in files:
                file_id = file.file_id
                filename = f"{get_size(file.file_size)} ᠰ {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{sumit}?start=subinps_-_-_-_{file_id}"),]
                )
        else:
            hancock = InlineKeyboardMarkup(
            [
                [
                     InlineKeyboardButton("☉ ʀᴇǫᴜᴇsᴛ", url="https://t.me/Reqstmovies"),
                     InlineKeyboardButton("☉ ʀᴇᴀᴅ", callback_data="cbrules")
                ]
            ]
        )
            rk = await message.reply_text("⭕️ ᴛʜɪs ᴍᴏᴠɪᴇ ɴᴏᴛ ғᴏᴜɴᴅ\n\n⭕️ ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴘᴇʟʟɪɴɢ ᴏɴ ɢᴏᴏɢʟᴇ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ\n\n⭕️ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴀᴅᴍɪɴ ғᴏʀ ᴜᴘʟᴏᴀᴅɪɴɢ", reply_markup=hancock)
            await asyncio.sleep(30)
            await rk.delete()
            await message.delete()
            return
        if not btn:
            return

        if len(btn) > 8: 
            btns = list(split_list(btn, 8)) 
            keyword = f"{message.chat.id}-{message.id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📄 ᴘᴀɢᴇs 1/1",callback_data="pages")]
            )
            if BUTTON:
                buttons.append([InlineKeyboardButton(text="◉ ᴄʟᴏsᴇ ◉",callback_data="close")])
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>ʜᴇʀᴇ ɪs ᴡʜᴀᴛ ɪ ғᴏᴜɴᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ғᴏʀ ʏᴏᴜʀ ǫᴜᴇʀʏ {search} </b>", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                r = await message.reply_text(f"⊚ <code>{search}</code> ᴜᴘʟᴏᴀᴅᴇᴅ\n\n⊚ ɴᴏᴛᴇ :- ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀғᴛᴇʀ 2 ᴍɪɴᴜᴛᴇ ᴛᴏ ᴀᴠᴏɪᴅ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs.\n\n", reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(120)
                await r.delete()
                await message.delete()
                return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="◉ ɴᴇxᴛ ◉",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📄 ᴘᴀɢᴇs 1/{data['total']}",callback_data="pages")]
        )
        if BUTTON:
            buttons.append([InlineKeyboardButton(text="◉ ᴄʟᴏsᴇ ◉",callback_data="close")])
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>ʜᴇʀᴇ ɪs ᴡʜᴀᴛ ɪ ғᴏᴜɴᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ғᴏʀ ǫᴜᴇʀʏ {search} ‌‎</b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            r = await message.reply_text(f"⊚ <code>{search}</code> ᴜᴘʟᴏᴀᴅᴇᴅ\n\n⊚ ɴᴏᴛᴇ :- ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀғᴛᴇʀ 2ᴍɪɴᴜᴛᴇs ᴛᴏ ᴀᴠᴏɪᴅ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs.", reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(120)
            await r.delete()
            await message.delete()


    if message.from_user.id not in subscriptions:
        if files:
            btn.append(
                    [
                        InlineKeyboardButton("✅ ʜᴏᴡ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ✅", url=f"https://t.me/TheMoviesUpdate/130")
                    ]
                    )
            btn.append(
                    [                                       
                        InlineKeyboardButton("⊙ ᴅɪʀᴇᴄᴛ ғɪʟᴇ|ᴄʟɪᴄᴋ ʜᴇʀᴇ ⊙", callback_data="Direct_file")
                    ] 
                    ) 
    
            for file in files:
                file_id = file.file_id
                filename = f"{get_size(file.file_size)} ᠰ {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=await get_shortlink(f"https://telegram.dog/{sumit}?start=subinps_-_-_-_{file_id}")),]
                )
        else:
            hancock = InlineKeyboardMarkup(
            [
                [
                     InlineKeyboardButton("☉ ʀᴇǫᴜᴇsᴛ", url="https://t.me/Reqstmovies"),
                     InlineKeyboardButton("☉ ʀᴇᴀᴅ", callback_data="cbrules")
                ]
            ]
        )
            rk = await message.reply_text("⭕️ ᴛʜɪs ᴍᴏᴠɪᴇ ɴᴏᴛ ғᴏᴜɴᴅ\n\n⭕️ ᴘʟᴇᴀsᴇ ᴄʜᴇᴄᴋ ʏᴏᴜʀ sᴘᴇʟʟɪɴɢ ᴏɴ ɢᴏᴏɢʟᴇ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ\n\n⭕️ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴀᴅᴍɪɴ ғᴏʀ ᴜᴘʟᴏᴀᴅɪɴɢ", reply_markup=hancock)
            await asyncio.sleep(30)
            await rk.delete()
            await message.delete()
            return
        if not btn:
            return

        if len(btn) > 8: 
            btns = list(split_list(btn, 8)) 
            keyword = f"{message.chat.id}-{message.id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📄 ᴘᴀɢᴇs 1/1",callback_data="pages")]
            )
            if BUTTON:
                buttons.append([InlineKeyboardButton(text="◉ ᴄʟᴏsᴇ ◉",callback_data="close")])
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>ʜᴇʀᴇ ɪs ᴡʜᴀᴛ ɪ ғᴏᴜɴᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ғᴏʀ ʏᴏᴜʀ ǫᴜᴇʀʏ {search} </b>", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                r = await message.reply_text(f"⊚ <code>{search}</code> ᴜᴘʟᴏᴀᴅᴇᴅ\n\n⊚ ɴᴏᴛᴇ :- ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀғᴛᴇʀ 2 ᴍɪɴᴜᴛᴇ ᴛᴏ ᴀᴠᴏɪᴅ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs.\n\n", reply_markup=InlineKeyboardMarkup(buttons))
                await asyncio.sleep(120)
                await r.delete()
                await message.delete()
                return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="◉ ɴᴇxᴛ ◉",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📄 ᴘᴀɢᴇs 1/{data['total']}",callback_data="pages")]
        )
        if BUTTON:
            buttons.append([InlineKeyboardButton(text="◉ ᴄʟᴏsᴇ ◉",callback_data="close")])
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>ʜᴇʀᴇ ɪs ᴡʜᴀᴛ ɪ ғᴏᴜɴᴅ ɪɴ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ғᴏʀ ǫᴜᴇʀʏ {search} ‌‎</b>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            r = await message.reply_text(f"⊚ <code>{search}</code> ᴜᴘʟᴏᴀᴅᴇᴅ\n\n⊚ ɴᴏᴛᴇ :- ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀғᴛᴇʀ 2ᴍɪɴᴜᴛᴇs ᴛᴏ ᴀᴠᴏɪᴅ ᴄᴏᴘʏʀɪɢʜᴛ ɪssᴜᴇs.", reply_markup=InlineKeyboardMarkup(buttons))
            await asyncio.sleep(120)
            await r.delete()
            await message.delete()

    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



# ------------------» ᴄᴀʟʟʙᴀᴄᴋ-ǫᴜᴇʀʏ «------------------ #

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("ʏᴏᴜ ᴀʀᴇ ᴜsɪɴɢ ᴛʜɪs ғᴏʀ ᴏɴᴇ  ᴏғ ᴍʏ ᴏʟᴅ ᴍᴇssᴀɢᴇ, ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴛʜᴇ ʀᴇǫᴜᴇsᴛ ᴀɢᴀɪɴ.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("◉ ʙᴀᴄᴋ ◉", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📄 ᴘᴀɢᴇs {int(index)+2}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="◉ ᴄʟᴏsᴇ ◉",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("◉ ʙᴀᴄᴋ ◉", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("◉ ɴᴇxᴛ ◉", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📄 ᴘᴀɢᴇs {int(index)+2}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="◉ ᴄʟᴏsᴇ ◉",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("ʏᴏᴜ ᴀʀᴇ ᴜsɪɴɢ ᴛʜɪs ғᴏʀ ᴏɴᴇ  ᴏғ ᴍʏ ᴏʟᴅ ᴍᴇssᴀɢᴇ, ᴘʟᴇᴀsᴇ sᴇɴᴅ ᴛʜᴇ ʀᴇǫᴜᴇsᴛ ᴀɢᴀɪɴ.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("◉ ɴᴇxᴛ ◉", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📄 ᴘᴀɢᴇs {int(index)}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="◉ ᴄʟᴏsᴇ ◉",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("◉ ʙᴀᴄᴋ ◉", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("◉ ɴᴇxᴛ ◉", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📄 ᴘᴀɢᴇs {int(index)}/{data['total']}", callback_data="pages")]
                )
                if BUTTON:
                    buttons.append([InlineKeyboardButton(text="◉ ᴄʟᴏsᴇ ◉",callback_data="close")])

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        


        elif query.data.startswith("subinps"):
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=get_size(files.file_size)
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                           InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇs', url="https://t.me/TheMoviesUpdate"),
                           InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ ', url="https://t.me/TheMoviesRequests")
                    ]
                    
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("<code>ɪ ʟɪᴋᴇ ʏᴏᴜʀ sᴍᴀʀᴛɴᴇss, ʙᴜᴛ ᴅᴏɴ'ᴛ ʙᴇ ᴏᴠᴇʀsᴍᴀʀᴛ 😒</code>",show_alert=True)
                return
            ident, file_id = query.data.split("#")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=get_size(files.file_size)
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{title}"
                buttons = [
                    [
                           InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇs', url="https://t.me/TheMoviesUpdate"),
                           InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ ', url="https://t.me/TheMoviesRequests")
                    ]
                    
                    ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )

        elif query.data=="home":
            buttons = [
        [
            InlineKeyboardButton("sɪʟᴠᴇʀ - 39ʀs|1 ᴍᴏɴᴛʜ", callback_data=f"alert_msg")
        ],
        [
            InlineKeyboardButton("ᴘʟᴀᴛɪɴᴜᴍ - 99ʀs|3 ᴍᴏɴᴛʜs", callback_data="alert_msg2"),            
        ],
        [
            InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", url="https://t.me/Reqstmovies"),
            InlineKeyboardButton("ʜᴏᴡ ᴛᴏ ᴘᴀʏ ᴍᴏɴᴇʏ", callback_data="help_pay"),            
  
        ],
    ]
            reply_markup = InlineKeyboardMarkup(buttons)
            try:
                await query.edit_message_text(
                    PLANS_TEXT,
                    reply_markup=reply_markup
            )
            except MessageNotModified:
                pass


        elif query.data=="help_pay":
            get_me = await client.get_me()
            USERNAME = get_me.username
            buttons = [
                [
                    InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴏᴡɴᴇʀ", url="https://t.me/Reqstmovies"),
                    InlineKeyboardButton("ǫʀ ᴄᴏᴅᴇ sᴄᴀɴ", url="https://graph.org/file/c9ce45d64cc8f278a1c00.jpg"),
                ],   
                [   
                    InlineKeyboardButton(" ᴄʟᴏsᴇ ", callback_data="close") ,
                    InlineKeyboardButton("⟲ ʙᴀᴄᴋ ⟳", callback_data="home")
                ]
           ]
            reply_markup = InlineKeyboardMarkup(buttons)
            try:
                await query.edit_message_text(
                    HOW_TO_PAY,
                    reply_markup=reply_markup
            )
            except MessageNotModified:
                pass


        

        elif query.data=="alert_msg":
            await query.answer("ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ᴛᴏ ᴀᴄᴛɪᴠᴀᴛᴇ ᴀɴʏ ᴘᴀɴɴᴇʟ !", show_alert=True)

        elif query.data=="alert_msg2":
            await query.answer("ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ ᴛᴏ ᴀᴄᴛɪᴠᴀᴛᴇ ᴀɴʏ ᴘᴀɴɴᴇʟ !", show_alert=True)

        elif query.data=="Direct_file":
            await query.answer("ɪғ ʏᴏᴜ ʙᴜʏ ᴘʟᴀɴ ᴛʜᴇɴ ʏᴏᴜ ɢᴇᴛ ᴅɪʀᴇᴄᴛ ᴍᴏᴠɪᴇs ғɪʟᴇ\nᴇɴᴊᴏʏ ʏᴏᴜʀ ᴘʟᴀɴ ᴀɴᴅ ɢᴇᴛ ᴍᴏʀᴇ ᴍᴏᴠɪᴇs ᴡɪᴛʜ ᴀᴅᴅ ғʀᴇᴇ\nᴛᴏ ᴄʜᴇᴄᴋ ᴀʟʟ ᴀᴠᴀɪʟᴀʙʟᴇ ᴘʟᴀɴs !!", show_alert=True)

        elif query.data == "pages":
            await query.answer()
        elif query.data == "close":
            try:
                await query.message.reply_to_message.delete()
                await query.message.delete()
            except:
                await query.message.delete()
                
    else:
        await query.answer("🥲 ᴊᴀᴀᴋᴇ ᴀᴘɴᴀ sᴇᴀʀᴄʜ ᴋʀᴏ 👀",show_alert=True)
