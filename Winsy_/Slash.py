import sqlite3
import discord
import asyncio
from discord_slash import SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle, ContextMenuType
from discord_slash.context import ComponentContext, MenuContext
from Winsy import bot, slash, my_id
from Winsy import all_guilds
import Winsy

conn = sqlite3.connect('./Winsy_/Winsy_main.db')
my_server_id = 762380604058632222

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

@slash.slash(
    name='spam',
    description='Spam a user for 10 times.',
    guild_ids=all_guilds,
    options=[
        create_option(
            name="user",
            description="Select the user to be spammed",
            required=True,
            option_type=6
        ),
        create_option(
            name="message",
            description='Write the message (optional)',
            required=False,
            option_type=3
        )
    ]
)
async def _spam(ctx: SlashContext, user: discord.Member, message: str=""):
    await Winsy.spam(ctx, member=user, message=message)

@slash.slash(
    name='ignore_owner_list',
    description='Check out the list of owners of `ignore` command.',
    guild_ids=all_guilds
)
async def _ignoreownerlist(ctx: SlashContext):
    await Winsy.ignoreownerlist(ctx)

@slash.slash(
    name='ignored_members_list',
    description="Check out the list of members who don't have access of bot's commands",
    guild_ids=all_guilds
)
async def _ignorelist(ctx: SlashContext):
    await Winsy.ignorelist(ctx)

@slash.slash(
    name='ignore',
    description='Add a user in the "ignored" list (you need to be an ignored command owner).',
    guild_ids=all_guilds,
    options=[
        create_option(
            name='user',
            description='Choose the user.',
            required=True,
            option_type=6
        )
    ]
)
async def _ignore(ctx: SlashContext, user: discord.Member):
    await Winsy.ignore(ctx, member=user)

@slash.slash(
    name='unignore',
    description='Remove a user from the ignored members list',
    guild_ids=all_guilds,
    options=[
        create_option(
            name='user',
            description='Choose the user.',
            required=True,
            option_type=6
        )
    ]
)
async def _unignore(ctx: SlashContext, user: discord.Member):
    await Winsy.unignore(ctx, member=user)

@slash.slash(
    name='clear_ignorelist',
    description='Clear the entire ignored list.',
    guild_ids=all_guilds
)
async def _clearignorelist(ctx: SlashContext):
    await Winsy.clearignorelist(ctx)

@slash.slash(
    name='roast',
    description='Roast someone :P',
    guild_ids=all_guilds,
    options=[
        create_option(
            name='user',
            description='Choose the user to roast.',
            required=True,
            option_type=6
        )
    ]
)
async def _roast(ctx: SlashContext, user: discord.Member):
    await Winsy.roast(ctx, member=user)

@slash.slash(
    name='laugh_at',
    description='Laugh at someone',
    guild_ids=all_guilds,
    options=[
        create_option(
            name='user',
            description='Choose the user to laugh at.',
            required=True,
            option_type=6
        )
    ]
)
async def _laugh(ctx: SlashContext, user: discord.Member):
    await Winsy.laugh(ctx,at='at', member=user)

@slash.slash(
    name='mute',
    description='Mute some chumps😎',
    guild_ids=all_guilds,
    options=[
        create_option(
            name='user',
            description='Choose the chump to mute.',
            required=True,
            option_type=6
        )
    ]
)
async def _mute(ctx: SlashContext, user: discord.Member):
    await Winsy.mute(ctx, member=user)

@slash.slash(
    name='unmute',
    description='Unmute those poor souls',
    guild_ids=all_guilds,
    options=[
        create_option(
            name='user',
            description='Choose the poor soul to unmute.',
            required=True,
            option_type=6
        )
    ]
)
async def _unmute(ctx: SlashContext, user: discord.Member):
    await Winsy.unmute(ctx, member=user)

@slash.slash(
    name='test',
    description='components',
    guild_ids=[my_server_id]
)
async def _test(ctx: SlashContext):
    buttons=[
        create_button(style=ButtonStyle.blurple, label='You are gae', custom_id="gae"),
        create_button(style=ButtonStyle.red, label='NO!', custom_id='no'),
        create_button(style=ButtonStyle.grey, label='YES!', custom_id='yes'),
        create_button(style=ButtonStyle.green, label='LMAO!', custom_id='lmao')
    ]
    action_row = create_actionrow(*buttons)
    msg = await ctx.send("Hehe", components=[action_row])
    def check(context: ComponentContext):
        return context.author_id == my_id
    try:
        button_ctx: ComponentContext = await wait_for_component(bot, components=action_row, timeout=10)
        await button_ctx.edit_origin(content=f'You pressed!! {button_ctx.component["label"]}', components=[])
        print('Component :', button_ctx.component)
        print('Component Type:', button_ctx.component_type)
        print('Custom id:', button_ctx.custom_id)
        print('Component id:', button_ctx.component_id)
    except asyncio.TimeoutError:
        await ctx.edit(content='You failed to respond within time', components=[])

with open('./TOKENS/bot_token.txt', 'r') as file:
    TOKEN = file.read()

bot.run(TOKEN)