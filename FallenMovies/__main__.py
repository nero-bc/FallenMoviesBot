import logging
import logging.config
import pyromod.listen

# -------------------» ʟᴏɴɢɢɪɴɢ-ᴄᴏɴғɪɢ «------------------- #

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.ERROR)

from pyrogram import types
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from TheHanCock.helpers.utils import Media
from config import SESSION, API_ID, API_HASH, BOT_TOKEN
from typing import Union, Optional, AsyncGenerator

# -------------------» ʜᴀɴᴄᴏᴄᴋ-ʙᴏᴛ-ᴄʟɪᴇɴᴛ «------------------- #

class TheHanCock(Client):

    def __init__(self):
        super().__init__(
            name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            workers=50,
            plugins={"root": "TheHanCock.plugins"},
            sleep_threshold=5,
        )

    async def start(self):
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        self.username = '@' + me.username
        print(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")

    async def stop(self, *args):
        await super().stop()
        print("Bot stopped. Bye.")

    async def iter_messages(
        self,
        chat_id: Union[int, str],
        limit: int,
        offset: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        
        current = offset
        while True:
            new_diff = min(200, limit - current)
            if new_diff <= 0:
                return
            messages = await self.get_messages(chat_id, list(range(current, current+new_diff+1)))
            for message in messages:
                yield message
                current += 1


app = TheHanCock()
app.run()
