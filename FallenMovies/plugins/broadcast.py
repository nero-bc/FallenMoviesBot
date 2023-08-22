import os
import time
import asyncio 
import logging 
import datetime
from config import ADMINS
from FallenMovies.helpers.database import *
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# -------------------» sᴛᴀᴛs «------------------- #

@Client.on_message(filters.command("stats") & filters.user(ADMINS))
async def get_stats(bot :Client, message: Message):
    sumit = await message.reply('**ᴀᴄᴄᴇssɪɴɢ ᴅᴇᴛᴀɪʟs....**')
    total_users = len(await get_served_users())
    await sumit.edit( text=f"⊚ ᴛᴏᴛᴀʟ ᴜsᴇʀs |`{total_users}`")


# -------------------» ʙʀᴏᴀᴅᴄᴀsᴛ «------------------- #

@Client.on_message(filters.command("broadcast") & filters.user(ADMINS) & filters.reply)
async def broadcast_(bot, message):
    users = await get_served_users()
    b_msg = message.reply_to_message
    status = await message.reply_text(
        text='Broadcasting your messages...'
    )
    start_time = time.time()
    done = 0
    blocked = 0
    deleted = 0
    failed = 0
    success = 0
    
    for user in users:
        success, reason = await broadcast_messages(int(user['user_id']), b_msg)
        if success:
            success += 1
        elif success is False:
            if reason == "Blocked":
                blocked += 1
            elif reason == "Deleted":
                deleted += 1
            elif reason == "Error":
                failed += 1
        done += 1
        
        if not done % 20:
            await status.edit(f"Broadcast in progress:\n\nTotal Users: {len(users)}\nCompleted: {done}/{len(users)}")
    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await status.edit(f"Broadcast completed:\n\nTotal Users: {len(users)}\nCompleted: {done}/{len(users)}\n\nTime taken: {time_taken}")



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
