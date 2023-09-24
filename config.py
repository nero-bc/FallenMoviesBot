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

# ---------» Bot Settings «--------- 
BUTTON = True
USE_CAPTION_FILTER = True


# ---------» MongoDb Information «---------
DATABASE_URI = "mongodb+srv://cerimi3097:cerimi3097@cluster0.eoz2qwn.mongodb.net/?retryWrites=true&w=majority"
DATABASE_NAME = "Cluster0"
COLLECTION_NAME = 'StupidBoi_Files'


# ---------» Bot Information «---------
SESSION = 'Media_search'
API_ID = "28587040"
API_HASH = "20f4a4a125d663eb14693cf716788400"
BOT_TOKEN = "5843548252:AAFLYdZSEHdlIQ1lEOG4X8p8YacLiESprLU"


# ---------» Admins, Channels, And Users «---------
PREMIUMS = [1988545170, 1895952308]
ADMINS = [1988545170, 1895952308]
CHANNELS = [-1001886568963]
auth_users = []
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
AUTH_CHANNEL = -1001971430705
AUTH_GROUPS = []


# ---------» ʟɪɴᴋ sʜᴏʀᴛɴᴇʀ ᴄᴏɴᴠᴇʀᴛᴇʀ «---------
URL_SHORTNER_API = environ.get("URL_SHORTNER_API", "https://publicearn.com/api?api")
URL_SHORTNER_API_KEY = environ.get("URL_SHORTNER_API_KEY", "15597af089977d7b56868867823be0b17c76d0f1")



# ---------» Pics Links «---------
default_pics_links = """
https://graph.org/file/5cc48ce60199bda2ba676.jpg

https://graph.org/file/db5e038720b1578759d7b.jpg

https://graph.org/file/b9468522b4a59624eb169.jpg

https://graph.org/file/164547bf9849d103b0061.jpg

https://graph.org/file/4974ac902f866c40e6197.jpg

https://graph.org/file/b64154792ca4b43e924f1.jpg

"""
PICS = (environ.get('PICS', default_pics_links)).split()


# ---------» Start Message «---------
default_start_msg = """
**♿Welcome to AnimeBot**

♿Your gateway to endless #anime and #hanime delights!

🚼Type a name, any name, and let the adventure begin!
"""
START_MSG = environ.get('START_MSG', default_start_msg)


# --------- Custom Captions---------
default_file_caption = """
📁 {file_name}]
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Explore the anime world with us!
Join now and enjoy unlimited anime and hanime.
Invite your friends too!
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
