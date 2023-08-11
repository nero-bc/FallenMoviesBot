import re
from os import environ

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# ---------» ʙᴏᴛ sᴇᴛᴛɪɴɢs «--------- 
BUTTON = True
USE_CAPTION_FILTER = True


# ---------» ᴍᴏɴɢᴏ ᴅʙ ɪɴғᴏʀᴍᴀᴛɪᴏɴ «---------
DATABASE_URI = "mongodb+srv://MrsFallenBot:MrsFallenBot@cluster0.hsedwn2.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "Cluster0"
COLLECTION_NAME = 'Fallen_Files'


# ---------» ʙᴏᴛ ɪɴғᴏʀᴍᴀᴛɪᴏɴ «---------
SESSION = 'Media_search'
API_ID = "18719789"
API_HASH = "a03c27be3e14aac40f62cb4e95207fae"
BOT_TOKEN = "5895914482:AAGWrQgS_JIpFeuM-A0M_NIL7hYLRxDH8Kk"


# ---------» ᴀᴅᴍɪɴs ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴜsᴇʀs «---------
PREMIUMS = [6109551937, 5416887843, 6018550523]
ADMINS = [6109551937, 5416887843, 6018550523]
CHANNELS = [-1001652627420, -1001896500605]
auth_users = []
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
AUTH_CHANNEL = -1001831916389
AUTH_GROUPS = []


# ---------» ʟɪɴᴋ sʜᴏʀᴛɴᴇʀ ᴄᴏɴᴠᴇʀᴛᴇʀ «---------
URL_SHORTNER_API = environ.get("URL_SHORTNER_API", "https://urlshortx.com/api?api")
URL_SHORTNER_API_KEY = environ.get("URL_SHORTNER_API_KEY", "c460f2f1a0f68b2c56cda7f12121c210ed10b08b")



# ---------» ᴘɪᴄs ʟɪɴᴋs «---------
default_pics_links = """
https://graph.org/file/5cc48ce60199bda2ba676.jpg

https://graph.org/file/db5e038720b1578759d7b.jpg

https://graph.org/file/b9468522b4a59624eb169.jpg

https://graph.org/file/164547bf9849d103b0061.jpg

https://graph.org/file/4974ac902f866c40e6197.jpg

https://graph.org/file/b64154792ca4b43e924f1.jpg

"""
PICS = (environ.get('PICS', default_pics_links)).split()


# ---------» sᴛᴀʀᴛ ᴍᴇsᴀᴀɢᴇs «---------
default_start_msg = """
ʜᴇʟʟᴏ 
ɪ ᴀᴍ ᴍᴏᴠɪᴇs ᴘʀᴏᴠɪᴅᴇʀ ʙᴏᴛ
ɪ ᴄᴀɴ ᴘʀᴏᴠɪᴅᴇ ᴀʟʟ ᴍᴏᴠɪᴇs  
ᴊᴜsᴛ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ 
ᴍᴀᴋᴇ ᴀᴅᴍɪɴ ᴀɴᴅ ᴇɴᴊᴏʏ ᴜɴʟɪᴍɪᴛᴇᴅ ᴍᴏᴠɪᴇs
"""
START_MSG = environ.get('START_MSG', default_start_msg)


# --------- ᴄᴜsᴛᴏᴍ ᴄᴀᴘᴛɪᴏɴ ---------
default_file_caption = """
📁 {file_name}]
━━━━━━━━━━━━━━━━━━━━━━━━━━━
ɪғ ʏᴏᴜ ʟɪᴋᴇ ᴠɪᴅᴇᴏ ᴛʜᴀɴ ᴘʟᴇᴀsᴇ 
ᴀᴅᴅ sᴏᴍᴇ ᴍᴇᴍʙᴇʀ ᴀɴᴅ sʜᴀʀᴇ ᴛʜᴇ ʟɪɴᴋ
━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

FILE_CAPTION = environ.get('CUSTOM_CAPTION_FILE', default_file_caption)


OMDB_API_KEY = environ.get("OMDB_API_KEY", "")
if FILE_CAPTION.strip() == "":
    CUSTOM_FILE_CAPTION=None
else:
    CUSTOM_FILE_CAPTION=FILE_CAPTION
if OMDB_API_KEY.strip() == "":
    API_KEY=None
else:
    API_KEY=OMDB_API_KEY
