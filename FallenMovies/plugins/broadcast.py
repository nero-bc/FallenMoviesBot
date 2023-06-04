import os
import time
import asyncio 
import logging 
import datetime
from config import ADMINS
from TheHanCock.helpers.database import db
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# -------------------» sᴛᴀᴛs «------------------- #

@Client.on_message(filters.command("stats") & filters.user(ADMINS))
async def get_stats(bot :Client, message: Message):
    mr = await message.reply('**ᴀᴄᴄᴇssɪɴɢ ᴅᴇᴛᴀɪʟs....**')
    total_users = await db.total_users_count()
    await mr.edit( text=f"⊚ ᴛᴏᴛᴀʟ ᴜsᴇʀs |`{total_users}`")


# -------------------» ʙʀᴏᴀᴅᴄᴀsᴛ «------------------- #

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_handler(bot: Client, m: Message):
    all_users = await db.get_all_users()
    broadcast_msg = m.reply_to_message
    sts_msg = await m.reply_text("ʙʀᴏᴀᴅᴄᴀsᴛ sᴛᴀʀᴛᴇᴅ !!") 
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    total_users = await db.total_users_count()
    async for user in all_users:
        sts = await send_msg(user['_id'], broadcast_msg)
        if sts == 200:
           success += 1
        else:
           failed += 1
        if sts == 400:
           await db.delete_user(user['_id'])
        done += 1
        if not done % 20:
           await sts_msg.edit(f"ʙʀᴏᴀᴅᴄᴀsᴛ ɪɴ ᴘʀᴏɢʀᴇss:\nᴛᴏᴛᴀʟ ᴜsᴇʀs: {total_users}\nᴛᴏᴛᴀʟ ʙʀᴏᴀᴅᴄᴀsᴛ: {done} / {total_users}\nsᴜᴄᴄᴇss: {success}\nғᴀɪʟᴇᴅ: {failed}")
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await sts_msg.edit(f"ʙʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ:\nᴄᴏᴍᴘʟᴇᴛᴇ ɪɴ `{completed_in}`.\n\nᴛᴏᴛᴀʟ ᴜsᴇʀs {total_users}\nᴛᴏᴛᴀʟ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ: {done} / {total_users}\nsᴜᴄᴄᴇss: {success}\nғᴀɪʟᴇᴅ: {failed}")


# -------------------» sᴇɴᴅ-ᴍᴇssᴀɢᴇ «------------------- #
           
async def send_msg(user_id, message):
    try:
        await message.copy(chat_id=int(user_id))
        return 200
    except FloodWait as e:
        await asyncio.sleep(e.value)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        logger.info(f"{user_id} : ᴅᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ")
        return 400
    except UserIsBlocked:
        logger.info(f"{user_id} : ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ")
        return 400
    except PeerIdInvalid:
        logger.info(f"{user_id} : ᴜsᴇʀ ɪᴅ ɪɴᴠᴀʟɪᴅ")
        return 400
    except Exception as e:
        logger.error(f"{user_id} : {e}")
        return 500
