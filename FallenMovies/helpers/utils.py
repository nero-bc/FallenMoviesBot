import re
import os
import PTN
import json
import aiohttp
import base64
import logging
import requests
from struct import pack
from pyrogram import enums
from pyrogram.types import Message, InlineKeyboardButton
from config import URL_SHORTNER_API_KEY, URL_SHORTNER_API
from pyrogram.errors import UserNotParticipant
from pyrogram.file_id import FileId
from pymongo.errors import DuplicateKeyError
from umongo import Instance, Document, fields
from motor.motor_asyncio import AsyncIOMotorClient
from marshmallow.exceptions import ValidationError
from config import DATABASE_URI, DATABASE_NAME, COLLECTION_NAME, USE_CAPTION_FILTER, AUTH_CHANNEL, API_KEY

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# -------------------» ᴍᴏɴɢᴏ-ᴅᴀᴛᴀʙᴀsᴇ «------------------- #

client = AsyncIOMotorClient(DATABASE_URI)
db = client[DATABASE_NAME]
instance = Instance.from_db(db)


# -------------------» ᴍᴇᴅɪᴀ-ᴄʟᴀss «------------------- #

@instance.register
class Media(Document):
    file_id = fields.StrField(attribute='_id')
    file_ref = fields.StrField(allow_none=True)
    file_name = fields.StrField(required=True)
    file_size = fields.IntField(required=True)
    file_type = fields.StrField(allow_none=True)
    mime_type = fields.StrField(allow_none=True)
    caption = fields.StrField(allow_none=True)

    class Meta:
        indexes = ('$file_name', )
        collection_name = COLLECTION_NAME


# -------------------» sᴀᴠᴇ-ғɪʟᴇ «------------------- #

async def save_file(media):
    """Save file in database"""

    file_id, file_ref = unpack_new_file_id(media.file_id)
    file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
    try:
        file = Media(
            file_id=file_id,
            file_ref=file_ref,
            file_name=file_name,
            file_size=media.file_size,
            file_type=media.file_type,
            mime_type=media.mime_type,
            caption=media.caption.html if media.caption else None,
        )
    except ValidationError:
        logger.exception('ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ ᴡʜɪʟᴇ sᴀᴠɪɴɢ ғɪʟᴇ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ.')
        return False, 2
    else:
        try:
            await file.commit()
        except DuplicateKeyError:      
            logger.warning(
                f'{getattr(media, "file_name", "NO_FILE")} ɪs ᴀʟʀᴇᴀᴅʏ sᴀᴠᴇᴅ ɪɴ ᴅᴀᴛᴀʙᴀsᴇ.'
            )

            return False, 0
        else:
            logger.info(f'{getattr(media, "file_name", "NO_FILE")} ɪs sᴀᴠᴇᴅ ᴛᴏ ᴅᴀᴛᴀʙᴀsᴇ.')
            return True, 1



# -------------------» sᴇᴀʀᴄʜ-ʀᴇsᴜʟᴛ «------------------- #

async def get_search_results(query, file_type=None, max_results=10, offset=0):
    """For given query return (results, next_offset)"""

    query = query.strip()
    if not query:
        raw_pattern = '.'
    elif ' ' not in query:
        raw_pattern = r'(\b|[\.\+\-_])' + query + r'(\b|[\.\+\-_])'
    else:
        raw_pattern = query.replace(' ', r'.*[\s\.\+\-_]')

    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except:
        return [], ''

    if USE_CAPTION_FILTER:
        filter = {'$or': [{'file_name': regex}, {'caption': regex}]}
    else:
        filter = {'file_name': regex}

    if file_type:
        filter['file_type'] = file_type

    total_results = await Media.count_documents(filter)
    next_offset = offset + max_results

    if next_offset > total_results:
        next_offset = ''

    cursor = Media.find(filter)    
    cursor.sort('$natural', -1)    
    cursor.skip(offset).limit(max_results)    
    files = await cursor.to_list(length=max_results)
    return files, next_offset


# -------------------» ɢᴇᴛ-ғɪʟᴛᴇʀ «------------------- #

async def get_filter_results(query):
    query = query.strip()
    if not query:
        raw_pattern = '.'
    elif ' ' not in query:
        raw_pattern = r'(\b|[\.\+\-_])' + query + r'(\b|[\.\+\-_])'
    else:
        raw_pattern = query.replace(' ', r'.*[\s\.\+\-_]')
    try:
        regex = re.compile(raw_pattern, flags=re.IGNORECASE)
    except:
        return []
    filter = {'file_name': regex}
    total_results = await Media.count_documents(filter)
    cursor = Media.find(filter)
    cursor.sort('$natural', -1)
    files = await cursor.to_list(length=int(total_results))
    return files


# -------------------» ғɪʟᴇ-ᴅᴇᴛᴀɪʟs «------------------- #

async def get_file_details(query):
    filter = {'file_id': query}
    cursor = Media.find(filter)
    filedetails = await cursor.to_list(length=1)
    return filedetails


# -------------------» ғᴏʀᴄᴇ-sᴜʙsᴄʀɪʙᴇᴅ «------------------- #

async def is_subscribed(bot, query):
    try:
        user = await bot.get_chat_member(AUTH_CHANNEL, query.from_user.id)
    except UserNotParticipant:
        pass
    except Exception as e:
        logger.exception(e)
    else:
        if not user.status == 'kicked':
            return True

    return False


# -------------------» ᴘᴏsᴛᴇʀ «------------------- #

async def get_poster(movie):
    extract = PTN.parse(movie)
    try:
        title=extract["title"]
    except KeyError:
        title=movie
    try:
        year=extract["year"]
        year=int(year)
    except KeyError:
        year=None
    if year:
        filter = {'$and': [{'title': str(title).lower().strip()}, {'year': int(year)}]}
    else:
        filter = {'title': str(title).lower().strip()}
    cursor = Poster.find(filter)
    is_in_db = await cursor.to_list(length=1)
    poster=None
    if is_in_db:
        for nyav in is_in_db:
            poster=nyav.poster
    else:
        if year:
            url=f'https://www.omdbapi.com/?s={title}&y={year}&apikey={API_KEY}'
        else:
            url=f'https://www.omdbapi.com/?s={title}&apikey={API_KEY}'
        try:
            n = requests.get(url)
            a = json.loads(n.text)
            if a["Response"] == 'True':
                y = a.get("Search")[0]
                v=y.get("Title").lower().strip()
                poster = y.get("Poster")
                year=y.get("Year")[:4]
                id=y.get("imdbID")
                await get_all(a.get("Search"))
        except Exception as e:
            logger.exception(e)
            pass
    return poster


# -------------------» ɢᴇᴛ-ᴀʟʟ «------------------- #

async def get_all(list):
    for y in list:
        v=y.get("Title").lower().strip()
        poster = y.get("Poster")
        year=y.get("Year")[:4]
        id=y.get("imdbID")
        await save_poster(id, v, year, poster)


# -------------------» ᴇɴᴄᴏᴅᴇ-ғɪʟᴇ «------------------- #

def encode_file_id(s: bytes) -> str:
    r = b""
    n = 0

    for i in s + bytes([22]) + bytes([4]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0

            r += bytes([i])

    return base64.urlsafe_b64encode(r).decode().rstrip("=")


# -------------------» ᴇɴᴄᴏᴅᴇ-ғɪʟᴇ-ʀᴇғ «------------------- #

def encode_file_ref(file_ref: bytes) -> str:
    return base64.urlsafe_b64encode(file_ref).decode().rstrip("=")


# -------------------» ᴜɴᴘᴀᴄᴋ-ɴᴇᴡ-ғɪʟᴇ «------------------- #

def unpack_new_file_id(new_file_id):
    """Return file_id, file_ref"""
    decoded = FileId.decode(new_file_id)
    file_id = encode_file_id(
        pack(
            "<iiqq",
            int(decoded.file_type),
            decoded.dc_id,
            decoded.media_id,
            decoded.access_hash
        )
    )
    file_ref = encode_file_ref(decoded.file_reference)
    return file_id, file_ref


# -------------------» ɢᴇᴛ-sɪᴢᴇ «------------------- #

def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])


# -------------------» sʜᴏʀᴛʟɪɴᴋ «------------------- #

async def get_shortlink(link):
    https = link.split(":")[0]
    if "http" == https:
        https = "https"
        link = link.replace("http", https)
    url = f'https://urlshortx.com/api?'
    params = {'api': URL_SHORTNER_API_KEY,
              'url': link,
              }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
                data = await response.json()
                if data["status"] == "success":
                    return data['shortenedUrl']
                else:
                    logger.error(f"Error: {data['message']}")
                    return f'{URL_SHORTNER_API}={URL_SHORTNER_API_KEY}&link={link}'

    except Exception as e:
        logger.error(e)
        return f'{URL_SHORTNER_API}={URL_SHORTNER_API_KEY}&link={link}'
