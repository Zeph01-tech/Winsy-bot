import sqlite3
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.context import MenuContext
from discord_slash.model import ContextMenuType
from Winsy import bot, slash
import Winsy

conn = sqlite3.connect('C:/Users/OMEN/Projekts/Winsy-Heroku/Winsy_/Winsy_main.db')
my_server_id = 762380604058632222

def fetch_guilds():
    cursor = conn.cursor()
    data = cursor.execute("""SELECT * FROM My_Guilds""").fetchall()
    guilds = []
    for guild_data in data:
        guilds.append(guild_data[-1])

    return guilds

all_guilds = fetch_guilds()

@slash.slash(
    name='ping',
    description='Check bot latency',
    guild_ids=all_guilds
)
async def _ping(ctx: SlashContext):
    await Winsy.ping(ctx)

@slash.slash(
    name='purge',
    description='Delete some clutter from your channel',
    guild_ids=all_guilds,
    options=[
        create_option(
            name="amount",
            description="Mention the amount of messages you wanna clear",
            required=True,
            option_type=4
        )
    ]
)
async def _purge(ctx: SlashContext, amount: int=None):
    await Winsy.purge(ctx, amount=amount, slash=True)

with open('./TOKENS/bot_token.txt', 'r') as file:
    TOKEN = file.read()

bot.run(TOKEN)