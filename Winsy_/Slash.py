import sqlite3
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash.context import MenuContext
from discord_slash.model import ContextMenuType
from Winsy import bot
import Winsy

conn = sqlite3.connect('C:/Users/OMEN/Projekts/winsy-bot/Winsy.db')
my_server_id = 762380604058632222
slash = SlashCommand(bot, sync_commands=True)

def fetch_guilds():
    cursor = conn.cursor()
    data = cursor.execute("""SELECT * FROM Guilds""").fetchall()
    guilds = []
    for guild_data in data:
        guilds.append(guild_data[-1])

    return guilds

@slash.slash(
    name='straight',
    description='See whether you are gae or straight',
    guild_ids=fetch_guilds(),
    options=[
        create_option(
            name="choose",
            description="Choose the type sexuality u have!",
            required=True,
            option_type=3,
            choices=[
                create_choice(name="gae", value="Lmao Mrityu"), create_choice(name="straight", value="Welp op")
            ]
        )
    ]
)
async def _lol(ctx: SlashContext, choose):
    await ctx.send(choose)

@slash.slash(
    name='ping',
    description="Check bot latency",
    guild_ids=fetch_guilds()
)
async def _ping(ctx: SlashContext):
    await Winsy.ping(ctx)

if __name__ == "__main__":
    with open("C:/Users/OMEN/Projekts/winsy-bot/TOKENS/token.txt") as file:
        TOKEN = file.read()
    bot.run(TOKEN)