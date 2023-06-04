import os
import logging
import asyncio
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from config import ADMINS
from FallenMovies.helpers.utils import save_file
from pyromod import listen
logger = logging.getLogger(__name__)
lock = asyncio.Lock()


# -------------------» ɪɴᴅᴇx «------------------- #

@Client.on_message(filters.private & filters.user(ADMINS) & filters.command('index'))
async def batch(client: Client, message: Message):
    if lock.locked():
        await message.reply("<code>ᴡᴀɪᴛ ᴜɴᴛɪʟ ᴘʀᴇᴠɪᴏᴜs ᴘʀᴏᴄᴇss ᴄᴏᴍᴘʟᴇᴛᴇ.</code>")
    else:
        while True:
            last_msg = await client.ask(text = "<code>ғᴏʀᴡᴀʀᴅ ʟᴀsᴛ ᴍsɢ ғʀᴏᴍ ᴅʙ ᴄʜᴀɴɴᴇʟ (ᴡɪᴛʜ ǫᴜᴏᴛᴇs) \n\nᴏʀ sᴇɴᴅ ᴛʜᴇ ᴅʙ ᴄʜᴀɴɴᴇʟ ᴘᴏsᴛ ʟɪɴᴋ</code>", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)        
            try:
                last_msg_id = last_msg.forward_from_message_id
                chat_id = last_msg.forward_from_chat.username or last_msg.forward_from_chat.id
                await client.get_messages(chat_id, last_msg_id)
                break
            except Exception as e:
                await last_msg.reply_text(f"<code>ᴛʜɪs ɪs ᴀɴ ɪɴᴠᴀʟɪᴅ ᴍᴇssᴀɢᴇ, ᴇɪᴛʜᴇʀ ᴛʜᴇ ᴄᴀʜɴɴᴇʟ ɪs ᴘʀɪᴠᴀᴛᴇ ᴀɴᴅ ʙᴏᴛ ɪs ɴᴏᴛ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ᴛʜᴇ ғᴏʀᴡᴀʀᴅᴇᴅ ᴄʜᴀᴛ, ᴏʀ ʏᴏᴜ ғᴏʀᴡᴀʀᴅᴇᴅ ᴍᴇssᴀɢᴇs ᴀs ᴄᴏᴘʏ.\nᴇʀʀᴏʀ ᴄᴀᴜsᴇᴅ ᴅᴜᴇ ᴛᴏ </code> <code>{e}</code>")
                continue

        msg = await message.reply('ᴘʀᴏᴄᴇssɪɴɢ...⏳')
        total_files = 0
        async with lock:
            try:
                total=last_msg_id + 1
                current=int(os.environ.get("SKIP", 2))
                nyav=0
                while True:
                    try:
                        message = await client.get_messages(chat_id=chat_id, message_ids=current, replies=0)
                    except FloodWait as e:
                        await asyncio.sleep(e.x)
                        message = await client.get_messages(
                            chat_id,
                            current,
                            replies=0
                            )
                    except Exception as e:
                        print(e)
                    try:
                        for file_type in ("document", "video", "audio"):
                            media = getattr(message, file_type, None)
                            if media is not None:
                                break
                            else:
                                continue
                        media.file_type = file_type
                        media.caption = message.caption
                        await save_file(media)
                        total_files += 1
                    except Exception as e:
                        print(e)
                    current+=1
                    nyav+=1
                    if nyav == 20:
                        await msg.edit(f"🖨️ ᴛᴏᴛᴀʟ ᴍᴇssᴀɢᴇs ғᴇᴛᴄʜᴇᴅ| {current}\n🎬 ᴛᴏᴛᴀʟ ᴍᴇssᴀɢᴇs sᴀᴠᴇᴅ| {total_files}")
                        nyav -= 20
                    if current == total:
                        break
                    else:
                        continue
            except Exception as e:
                logger.exception(e)
                await msg.edit(f'ᴇʀʀᴏʀ: {e}')
            else:
                await msg.edit(f"🎬 ᴛᴏᴛᴀʟ {total_files} sᴀᴠᴇᴅ ᴛᴏ ᴅᴀᴛᴀʙᴀsᴇ")
