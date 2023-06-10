import logging
from os import environ, mkdir, path, sys
#from dotenv import load_dotenv
from pyrogram import Client
from os import getenv

#j
import time

from dotenv import load_dotenv
from telethon import TelegramClient, events, functions, types

formatter = logging.Formatter('%(levelname)s %(asctime)s - %(name)s - %(message)s')

fh = logging.FileHandler(f'{__name__}.log', 'w')
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.INFO)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.addHandler(ch)

telethon_logger = logging.getLogger("telethon")
telethon_logger.setLevel(logging.WARNING)
telethon_logger.addHandler(ch)
telethon_logger.addHandler(fh)

botStartTime = time.time()
load_dotenv()



# Log
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()],
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)
# Mandatory Variable
try:
    API_ID = int(environ["API_ID", "11984338"])
    API_HASH = environ["API_HASH", "ea4cb0f090d7366f7e4ab9dfc116acc7"]
    BOT_TOKEN = environ["BOT_TOKEN", "5764337430:AAErAYClzy1xB_iH1Up2mN2kEIKGjNqymRY"]
except KeyError:
    LOGGER.debug("One or More ENV variable not found.")
    sys.exit(1)
    
AUTH_CHATS = environ.get("AUTH_CHATS", "-1001976490968").split()
AUTH_CHATS = [int(_x) for _x in AUTH_CHATS]
OPENAI_API = getenv("OPENAI_API", "")


vvv

bot = TelegramClient(__name__, API_ID, API_HASH, base_logger=telethon_logger).start(bot_token=BOT_TOKEN)
logger.info("TELETHON BOT STARTED BROOO")


class Mbot(Client):
    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            ":memory:",
            plugins=dict(root=f"{name}/plugins"),
            workdir="./cache/",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            sleep_threshold=30,
        )
    async def start(self):
        global BOT_INFO
        await super().start()
        BOT_INFO = await self.get_me()
        if not path.exists("/tmp/thumbnails/"):
            mkdir("/tmp/thumbnails/")
        for chat in AUTH_CHATS:
            await self.send_photo(
                chat,
                "https://telegra.ph/file/2a873c12ce89099af82aa.jpg",
                "**Bot Started.**",
            )
        LOGGER.info(f"PYROGRAM BOT STARTED As {BOT_INFO.username}\n")
    async def stop(self, *args):
        await super().stop()
        LOGGER.info("BOT STOPPED, BYE.")

        
