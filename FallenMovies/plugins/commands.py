import os
import asyncio
import random
import logging
from pyrogram import Client, filters, enums
from pyrogram.errors import UserNotParticipant, FloodWait, UserIsBlocked, InputUserDeactivated
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from config import PICS, START_MSG, CHANNELS, ADMINS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION
from FallenMovies.helpers.utils import Media, get_file_details, get_size
logger = logging.getLogger(__name__)


# -------------------» ғᴏʀᴄᴇ-ᴍᴇssᴀɢᴇ «------------------- #

FORCE_MSG = """
<code>ʜᴇʏ 
ᴀᴄᴄᴏʀᴅɪɴɢ ᴛᴏ ᴍʏ ᴅᴀᴛᴀʙᴀsᴇ ʏᴏᴜ'ᴠᴇ ɴᴏᴛ ᴊᴏɪɴᴇᴅ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ʏᴇᴛ, ɪғ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴜsᴇ ᴍᴇ ᴛʜᴇɴ ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ᴀɴᴅ sᴛᴀʀᴛ ᴍᴇ ᴀɢᴀɪɴ !</code>
"""


# -------------------» sᴛᴀʀᴛ «------------------- #

@Client.on_message(filters.command("start"))
async def start(bot, cmd):
    usr_cmdall1 = cmd.text
    if usr_cmdall1.startswith("/start subinps"):
        if AUTH_CHANNEL:
            invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
            try:
                user = await bot.get_chat_member(int(AUTH_CHANNEL), cmd.from_user.id)
                if user.status == "kicked":
                    await bot.send_message(
                        chat_id=cmd.from_user.id,
                        text="Sorry Sir, You are Banned to use me.",
                        parse_mode=enums.ParseMode.MARKDOWN,
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                ident, file_id = cmd.text.split("_-_-_-_")
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text=FORCE_MSG,
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🤖 ᴊᴏɪɴ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ", url=invite_link.invite_link)
                            ],
                            [
                                InlineKeyboardButton(" 🔄 ᴛʀʏ ᴀɢᴀɪɴ", callback_data=f"checksub#{file_id}")
                            ]
                        ]
                    ),
                    parse_mode=enums.ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
                return
            except Exception:
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="Something went Wrong.",
                    parse_mode=enums.ParseMode.MARKDOWN,
                    disable_web_page_preview=True
                )
                return
        try:
            ident, file_id = cmd.text.split("_-_-_-_")
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
                await bot.send_cached_media(
                    chat_id=cmd.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        except Exception as err:
            await cmd.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")
    elif len(cmd.command) > 1 and cmd.command[1] == 'subscribe':
        invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text={FORCE_MSG},
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🤖 Jᴏɪɴ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ", url=invite_link.invite_link)
                    ]
                ]
            )
        )
    else:
        await cmd.reply_photo(
            photo=random.choice(PICS),
            caption=START_MSG,
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕", url=f"https://t.me/TheHanCockBot?startgroup=true")
                    ],
        
                    [
                        InlineKeyboardButton("🗯️ ᴜᴘᴀᴅᴛᴇs", url="https://t.me/TheMoviesUpdate"),
                        InlineKeyboardButton("🎡 sᴜᴘᴘᴏʀᴛ", url="https://t.me/TheMoviesRequests")
                    ]
                    ]
               )
        )



# -------------------» ᴄʜᴀɴɴᴇʟ «------------------- #

@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **ɪɴᴅᴇxᴇᴅ ᴄʜᴀɴɴᴇʟs|ɢʀᴏᴜᴘs**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**ʜᴇʀᴇ:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)



# -------------------» ᴛᴏᴛᴀʟ «------------------- #

@Client.on_message(filters.command('total') & filters.user(ADMINS))
async def total(bot, message):
    """Show total files in database"""
    msg = await message.reply("ᴘʀᴏᴄᴇssɪɴɢ...⏳", quote=True)
    try:
        total = await Media.count_documents()
        await msg.edit(f'📁 sᴀᴠᴇᴅ ғɪʟᴇs: {total}')
    except Exception as e:
        logger.exception('ғᴀɪʟᴇᴅ ᴛᴏ ᴄʜᴇᴄᴋ ᴛᴏᴛᴀʟ ғɪʟᴇs.')
        await msg.edit(f'ᴇʀʀᴏʀ: {e}')



# -------------------» ʟᴏɢɢᴇʀ «------------------- #

@Client.on_message(filters.command('logger') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))


# -------------------» ᴅᴇʟᴇᴛᴇ «------------------- #

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("ᴘʀᴏᴄᴇssɪɴɢ...⏳", quote=True)
    else:
        await message.reply('ʀᴇᴘʟʏ ᴛᴏ ғɪʟᴇ ᴡɪᴛʜ /delete ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴅᴇʟᴇᴛᴇ', quote=True)
        return

    for file_type in (enums.MessageMediaType.VIDEO, enums.MessageMediaType.AUDIO, enums.MessageMediaType.DOCUMENT):
        media = getattr(reply, file_type.value, None)
        if media is not None:
            break
    else:
        await msg.edit('ᴛʜɪs ɪs ɴᴏᴛ sᴜᴘᴘᴏʀᴛᴇᴅ ғɪʟᴇ ғᴏʀᴍᴀᴛ')
        return

    result = await Media.collection.delete_many({
        'file_name': media.file_name,
        'file_size': media.file_size,
        'mime_type': media.mime_type
    })
    if result.deleted_count:
        await msg.edit('ғɪʟᴇ ɪs sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ғʀᴏᴍ ᴅᴀᴛᴀʙᴀsᴇ')
    else:
        await msg.edit('ғɪʟᴇ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ')


# -------------------» ᴅᴇʟᴇᴛᴇ-ᴀʟʟ «------------------- #

@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'ᴛʜᴜs ᴡɪʟʟ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ɪɴᴅᴇxᴇᴅ ғɪʟᴇs.\n\nᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴄᴏɴᴛɪɴᴜᴇ??',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="✅ ʏᴇᴀʜ", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="❌ ɴᴏᴘᴇ", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )


# -------------------» ᴄᴀʟʟʙᴀᴄᴋ-ʀᴇɢᴇx «------------------- #

@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.answer()
    await message.message.edit('sᴜᴄᴄᴇssᴅᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ᴀʟʟ ᴛʜᴇ ɪɴᴅᴇxᴇᴅ ғɪʟᴇs.')



@Client.on_callback_query(filters.regex("cbrules"))
async def cbrules(_, query: CallbackQuery):
    await query.answer(
        f"""⚠️ ɪᴍᴘᴏʀᴛᴀɴᴛ ᴍᴇssᴀɢᴇ ʀᴇᴀᴅ ⚠️
sᴇɴᴅ ᴇxᴀᴄᴛ ɴᴀᴍᴇ ᴀɴᴅ ᴏɴʟy ᴍᴏᴠɪᴇ ɴᴀᴍᴇ ᴡɪᴛʜ yᴇᴀʀ ᴏʀ ʟᴀɴɢᴜᴀɢᴇ. (ᴄʜᴇᴄᴋ ᴄᴏʀʀᴇᴄᴛ ꜱᴩᴇʟʟɪɴɢ ꜱᴀᴍᴇ ᴀꜱ ɪɴ ɢᴏᴏɢʟᴇ) ᴅᴏɴᴛ ᴀᴅᴅ ᴀɴy ᴇxᴛʀᴀ ᴡᴏʀᴅꜱ ᴡʜɪʟᴇ ʀᴇǫᴜᴇꜱᴛɪɴɢ. ᴏᴛʜᴇʀᴡɪꜱᴇ yᴏᴜ ᴅᴏɴᴛ ɢᴇᴛ ᴛʜᴇ ᴍᴏᴠɪᴇ ᴄᴏʀʀᴇᴄᴛʟy 🚫 
ɪғ ᴍᴏᴠɪᴇ ɴᴏᴛ ғᴏᴜɴᴅ ᴛʜᴇɴ ʏᴏᴜ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴏᴡɴᴇʀ  
""", show_alert=True,
    )
