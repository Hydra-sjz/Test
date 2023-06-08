import logging
from os import environ, mkdir, path, sys
#from dotenv import load_dotenv
from pyrogram import Client
from os import getenv


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
    API_ID = int(environ["API_ID"])
    API_HASH = environ["API_HASH"]
    BOT_TOKEN = environ["BOT_TOKEN"]
except KeyError:
    LOGGER.debug("One or More ENV variable not found.")
    sys.exit(1)
    
AUTH_CHATS = environ.get("AUTH_CHATS", "-1001576243355").split()
AUTH_CHATS = [int(_x) for _x in AUTH_CHATS]
OPENAI_API = getenv("OPENAI_API", "")

#anime bot
ANILIST_CLIENT = os.environ.get("ANILIST_CLIENT")
ANILIST_SECRET = os.environ.get("ANILIST_SECRET")
ANILIST_REDIRECT_URL = os.environ.get("ANILIST_REDIRECT_URL", "https://anilist.co/api/v2/oauth/pin")
DB_URL = os.environ.get("DB_URL")
BOT_NAME = os.environ.get("BOT_NAME", "spoti")
TRIGGERS = os.environ.get("TRIGGERS", "/ !").split()


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

        
HELP_DICT['Group'] = '''
Group based commands:
/settings - Toggle stuff like whether to allow 18+ stuff in group or whether to notify about aired animes, etc and change UI
/disable - Disable use of a cmd in the group (Disable multiple cmds by adding space between them)
`/disable anime anilist me user`
/enable - Enable use of a cmd in the group (Enable multiple cmds by adding space between them)
`/enable anime anilist me user`
/disabled - List out disabled cmds
'''
HELP_DICT["Additional"] = """Use /reverse cmd to get reverse search via tracemoepy API
__Note: This works best on uncropped anime pic,
when used on cropped media, you may get result but it might not be too reliable__
Use /schedule cmd to get scheduled animes based on weekdays
Use /watch cmd to get watch order of searched anime
Use /fillers cmd to get a list of fillers for an anime
Use /quote cmd to get a random quote
"""
HELP_DICT["Anilist"] = """
Below is the list of basic anilist cmds for info on anime, character, manga, etc.
/anime - Use this cmd to get info on specific anime using keywords (anime name) or Anilist ID
(Can lookup info on sequels and prequels)
/anilist - Use this cmd to choose between multiple animes with similar names related to searched query
(Doesn't includes buttons for prequel and sequel)
/character - Use this cmd to get info on character
/manga - Use this cmd to get info on manga
/airing - Use this cmd to get info on airing status of anime
/top - Use this cmd to lookup top animes of a genre/tag or from all animes
(To get a list of available tags or genres send /gettags or /getgenres
'/gettags nsfw' for nsfw tags)
/user - Use this cmd to get info on an anilist user
/browse - Use this cmd to get updates about latest animes
"""
HELP_DICT["Oauth"] = """
This includes advanced anilist features
Use /auth or !auth cmd to get details on how to authorize your Anilist account with bot
Authorising yourself unlocks advanced features of bot like:
- adding anime/character/manga to favourites
- viewing your anilist data related to anime/manga in your searches which includes score, status, and favourites
- unlock /flex, /me, /activity and /favourites commands
- adding/updating anilist entry like completed or plan to watch/read
- deleting anilist entry
Use /flex or !flex cmd to get your anilist stats
Use /logout or !logout cmd to disconnect your Anilist account
Use /me or !me cmd to get your anilist recent activity
Can also use /activity or !activity
Use /favourites or !favourites cmd to get your anilist favourites
"""
