import sqlite3
import discord
import random
import asyncio
import os
import bitly_api
import requests
from youtube_dl import YoutubeDL
from youtube_search import YoutubeSearch
from spellchecker import SpellChecker
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import create_select, create_select_option
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext, MenuContext
from discord_slash.model import ContextMenuType

intents = discord.Intents.all()
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("T ", "t "), case_sensitive=True, intents=intents)
slash = SlashCommand(bot, sync_commands=True)
bot.remove_command('help')

conn = sqlite3.connect("./Winsy_/Winsy.db")

my_id = 762372102204030986
winsy_id = 873504810278739988
chizu_id = 896826940328128523

my_server_id = 762380604058632222

error_channel_id = 887385480679788574

bro_fist_replies = ["**Yesss boss!**", "**BRO FIST!!!**", "**Zhong Zhong**"]
good_night_replies = ["**Oyasumi!**", "**Night!**", "**Have a great night**", "**Sweet dreams**"]

good_night_gifs = ["https://c.tenor.com/3fAZZncIHDQAAAAC/smile-anime.gif", "https://c.tenor.com/ouo5podnrgUAAAAS/cuddle-love.gif", "https://c.tenor.com/01cElrH1Ed8AAAAS/anime-shiro.gif", "https://c.tenor.com/Bn_E6t9-m_wAAAAC/sleeping-kiss.gif", "https://c.tenor.com/3eouI6QChiEAAAAC/anime-cuteness.gif", "https://c.tenor.com/tVBrvOB5ttkAAAAC/11-sad.gif"]
laugh_command_gifs = ["https://cdn.discordapp.com/attachments/873552851157254144/874619767749758986/hehe.gif", "https://c.tenor.com/fqRNsILmXHQAAAAC/anime-girl.gif", "https://cdn.discordapp.com/attachments/873552851157254144/874620123930038282/natsu-lol.gif", "https://c.tenor.com/qEfogXAprQoAAAAC/nichijou-laughing.gif", "https://c.tenor.com/fbWCY-1exTsAAAAS/bokura-wa-minna-kawaisou-gifs-to-reaction.gif"]

def fetch_guilds():
    cursor = conn.cursor()
    data = cursor.execute("""SELECT * FROM My_Guilds""").fetchall()
    guilds = []
    for guild_data in data:
        guilds.append(guild_data[-1])

    return guilds

all_guilds = fetch_guilds()

class Embeds:
    def command_cancelled():
        return discord.Embed(description="Command cancelled.", color=0xe80e24)

    def non_dm_embed():
        return discord.Embed(title='Note.', description="Commands can't be used through dms.", color=color())

def color():  
    return random.choice([0xFF355E,0xFD5B78,0xFF6037,0xFF9966,0xFF9933,0xFFCC33,0xFFFF66,0xFFFF66,0xCCFF00,0x66FF66,0xAAF0D1,0x50BFE6,0xFF6EFF,0xEE34D2,0xFF00CC,0xFF00CC,0xFF3855,0xFD3A4A,0xFB4D46,0xFA5B3D,0xFFAA1D,0xFFF700,0x299617,0xA7F432,0x2243B6,0x5DADEC,0x5946B2,0x9C51B6,0xA83731,0xAF6E4D,0xBFAFB2,0xFF5470,0xFFDB00,0xFF7A00,0xFDFF00,0x87FF2A,0x0048BA,0xFF007C,0xE936A7])

def get_emoji(id):
    for emoji in my_guild.emojis:
        if emoji.id == id:
            return emoji

async def fetch_roasts(member_id):
    if member_id == my_id:
        type = 'Yash victim'
    else:
        type = 'Normal'

    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM roasts WHERE type = ?""", [type])
    roasts = []
    response = cursor.fetchall()
    for elm in response:
        roasts.append(elm[-1])
    dict = {"roasts" : roasts, "type" : type}
    return dict

def yt_quality_options(dict):
    quality_options = []
    for key in dict:
        quality_options.append(create_select_option(label=f"{key}. {dict[key]['quality']} ({dict[key]['size']})", value=str(key)))
    
    return quality_options

async def embed_maker(dict=None, link=None):
    if dict != None:
        dialouge = "**All the available qualities, send an index of the quality you want.**"
        quality_dialouge = ""
        for key in dict:
            quality_dialouge += f"\n*{key}*. {dict[key]['quality']} ({dict[key]['size']})"
        
        embed = discord.Embed(description=dialouge+quality_dialouge, color=color())

    elif link != None:
        choice = link[-5:] 
        link = link[0:-5]
        emoji2 = get_emoji(774306825708765184)
        embed = discord.Embed(description=f'**URL of the {choice} you searched for {emoji2}: {link}**', color=color())
        embed.set_footer(icon_url='https://cdn.discordapp.com/emojis/892776197887524935.png', text='Enjoy')

    return embed

async def shorten_url(url):
    with open('./TOKENS/bitly_token.txt', 'r') as file:
        token = file.read()
    conn = bitly_api.Connection(access_token=token)
    reponse = conn.shorten(url)
    new_url = reponse['url']
    return new_url

async def register_server(guild):
    cursor = conn.cursor()
    data = cursor.execute("""SELECT * FROM My_Guilds""").fetchall()
    for guild_data in data:
        if guild_data[-1] == guild.id:
            return
    cursor.execute("""INSERT INTO My_Guilds (Guild_Name, Guild_ID) VALUES (?, ?)""", [guild.name, guild.id])
    conn.commit()

@bot.event
async def on_ready():
    global my_guild
    for guild in bot.guilds:
        await register_server(guild)

    my_guild = await bot.fetch_guild(my_server_id)
    print("I'm logged in yay!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="winsy help"))

@bot.command()
async def help(ctx, *, category = None):
    sus_booty = get_emoji(892751786719469598)
    booty = get_emoji(885592612692709406)
    hyped = get_emoji(892750347599233034)
    rem = get_emoji(892776197887524935)
    if category is None:
        embed = discord.Embed(title="***Help panel***", description="List of categories of all commands", color=color())
        embed.add_field(name=f"*mention commands {sus_booty}*", value="`winsy help 1`", inline=False)
        embed.add_field(name=f"*interactive commands {booty}*", value="`winsy help 2`", inline=False)
        embed.add_field(name=f"*search commands {hyped}*", value="`winsy help 3`", inline=False)
        embed.add_field(name=f"*utility commands {rem}*", value='`winsy help 4`', inline=False)
        embed.set_footer(text="type a command along with category name")
        await ctx.send(embed=embed)
    
    elif category == '1':
        embed = discord.Embed(title="***Mention commands***", description="All mention commands.", color=color())
        embed.add_field(name="`gae <user mention> Possible aliase(s): 'gay'", value="*Gives the gay percentage of the mentioned user*", inline=False)
        embed.add_field(name="`roast <user mention>`", value="*Sends a random roast to the mentioned user*", inline=False)
        embed.add_field(name="`spam <user mention> <message(if any)>`", value="*Spams the message along with the mentioned user*", inline=False)
        embed.add_field(name="`poop at <user mention>`", value="*Poops in the dm of the mentioned user*", inline=True)
        await ctx.send(embed=embed)

    elif category == '2':
        embed = discord.Embed(title="**Interactive commands**", description="All the commands to interact with the bot.", color=color())
        embed.add_field(name="`goodnight` Possible aliase(s): `gn`, `oyasumi` ", value="*Winsy wishes goodnight*", inline=False)
        embed.add_field(name="`laugh at <user>`", value="*Winsy laughs at the mentioned user*", inline=False)
        embed.add_field(name="`brofist`", value="*Winsy wishes **brofist***", inline=False)
        embed.add_field(name="`why insult <user>`", value="*Winsy explains the reason to laugh at the <user>*", inline=False)
        await ctx.send(embed=embed)

    elif category == '3':
        embed = discord.Embed(title="**Search commands**", description="All the search commands", color=color())
        embed.add_field(name="`insta <insta post/reel link>`", value="Sends the media link for the user to download", inline=False)
        embed.add_field(name='`yt <vid link>`', value="Sends the media link for the user to download", inline=False)
        await ctx.send(embed=embed)

    elif category == '4':
        embed = discord.Embed(title="**Utility commands**", description="All the utility commands", color=color())
        embed.add_field(name='`ignore <user>`', value="User will be added in `ignored members list` (you need to be an `ignore cmd owner` to use this command)", inline=False)
        embed.add_field(name='`unignore <user>`', value="User will be removed from `ignored members list` (you need to be an `ignore cmd owner` to use this command)", inline=False)
        embed.add_field(name='`ignorelist` Possible aliase(s): `il`', value="Sends the list of all the currently ignored members", inline=False)
        embed.add_field(name='`ignoreownerlist` Possible aliase(s): `iol`', value="Sends the list of all the members who can use `ignore` command", inline=False)
        embed.add_field(name='`addignoreowner <user>` Possible aliase(s): `addio`', value="User will be added in the list of `ignore cmd owner(s)` (can only be used by bot owner)", inline=False)
        embed.add_field(name='`removeignoreowner <user>` Possible aliase(s): `removeio`', value="User will be removed from the list of `ignore cmd owner(s)` (can only be used by bot owner)", inline=False)
        embed.add_field(name="`kick <user>`", value="User will be kicked from the server (can only be used by members with thse `kick members` permission)", inline=False)
        embed.add_field(name="`mute <user>`", value="User will be muted (can only be used by members with `kick members` permission)", inline=False)
        embed.add_field(name="`unmute <user>`", value="User will be unmuted if already muted (can only be used by members with `kick members` permission)", inline=False)
        await ctx.send(embed=embed)
          
    await ctx.message.delete()

@commands.cooldown(1, 60, commands.BucketType.member)
@bot.command()
async def poop(ctx, at:str=None, member:discord.Member=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())

    else:
        guild_id = ctx.guild.id
        if guild_id not in ignored.guilds:
            ignored.addguild(guild_id)
        if ctx.author.id in ignored.guilds[guild_id]:
            return
        else:
            if at.lower() == 'at':
                if member is not None:
                    if member.id != my_id:
                        await member.send(":poo:")
                        await asyncio.sleep(4)
                        await member.send("*Flies away :bird:....*")
                        await ctx.send(f"Succesfully pooped at {member.mention}'s dm")
                    
                    else:

                        if ctx.author.id != my_id:
                            await ctx.send(f"Succesfully pooped at {member.mention}'s dm")
                            await asyncio.sleep(2)
                            await ctx.send(f"Well there's a twist, {ctx.author.mention} will understand ( ͡° ͜ʖ ͡°)")
                            await ctx.author.send("So you are the one who tried to make me poop in my master's dm huh?")
                            await asyncio.sleep(2)
                            await ctx.author.send("I'll rather poop in this shitty dm instead")
                            await asyncio.sleep(2)
                            await ctx.author.send(":poo:")
                            await asyncio.sleep(2)
                            await ctx.author.send("*HEHE flies away :bird:....*")
                
                        else:
                            await ctx.send("What do I call this, poop fetish? senpai?")

                else:
                    await ctx.send("You need to mention a user to poop on.")
            else:
                return

class ignoreable:
    members = [my_id]

class ignored:
    guilds = {}
    def guildkeys():
            keys = []
            for key in ignored.guilds:
                keys.append(key)
            return keys
    def addguild(guildid):
        value = {guildid : []}
        ignored.guilds.update(value)

@bot.command(aliases=['iol'])
async def ignoreownerlist(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())

    else:
        guild_id = ctx.guild.id
        if guild_id not in ignored.guilds:
            ignored.addguild(guild_id)
        if ctx.author.id in ignored.guilds[guild_id]:
            return
        else:
            embed = discord.Embed(title='**Owner list**', color=discord.Color.dark_red())
            ctr = 1
            dialouge = ''
            for id in ignoreable.members:
                try:
                    owner = await ctx.guild.fetch_member(id)
                    dialouge += f'{ctr}. *{owner.name}*\n'
                    ctr += 1
                except:
                    pass
            embed.add_field(name=f'List of all owners of `ignore` cmd {get_emoji(876032718486507591)}', value=dialouge, inline=False)
            await ctx.send(embed=embed)

@bot.command(aliases=['addio'])
async def addignoreowner(ctx, member:discord.Member=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())

    else:
        if ctx.author.id != my_id:
            return
        else:
            if member == None:
                await ctx.send('Mention a user to make `ignore cmd owner` {}'.format(get_emoji(885592462599536701)))
            else:
                if member.id not in ignoreable.members:
                    ignoreable.members.append(member.id)
                    await ctx.send("{} Now you are an owner of ignore command {}".format(member.mention, get_emoji(random.choice([881253669083955221, 876032718486507591, 892776197887524935]))))
                else:
                    await ctx.send('{} is already an owner of ignore command'.format(member.mention))

@bot.command(aliases=['removeio'])
async def removeignoreowner(ctx, member:discord.Member=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())

    else:
        if ctx.author.id != my_id:
            return
        else:
            if member == None:
                await ctx.send('Mention a user to remove from `ignore` owner list {}'.format(get_emoji(885592462599536701)))
            else:
                index = ignoreable.members.index(member.id)
                ignoreable.members.pop(index)
                await ctx.send('{} has been removed from ignore command owners list'.format(member.mention))

@bot.command(aliases=['il'])
async def ignorelist(ctx):
        if isinstance(ctx.channel, discord.channel.DMChannel):
            await ctx.send(embed=Embeds.non_dm_embed())

        else:
            guild_id = ctx.guild.id
            embed = discord.Embed(title='**List of ignored members in this server**', color=discord.Color.darker_grey())
            if guild_id not in ignored.guildkeys():
                ignored.addguild(guild_id)
            if ctx.author.id in ignored.guilds[guild_id]:
                return
            else:
                if ignored.guilds[guild_id] == []:
                    embed.description = '*Empty*'
                    await ctx.send(embed=embed)
                else:
                    ctr = 1
                    dialouge = ''
                    for id in ignored.guilds[guild_id]:
                        try:
                            baka = await ctx.guild.fetch_member(id)
                            dialouge += f'{ctr}. *{baka.name}*\n'
                            ctr += 1
                        except:
                            pass
                    if dialouge == '':
                        embed.description = '*Empty*'
                    else:
                        embed.add_field(name=f'{get_emoji(890869939429314610)}', value=dialouge, inline=False)
                    
                    await ctx.send(embed=embed)

@bot.command()
async def ignore(ctx, member:discord.Member=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())

    else:
        guild_id = ctx.guild.id
        if ctx.author.id not in ignoreable.members:
            return
        else:
            if member == None:
                await ctx.send('Mention a user to ignore {}'.format(get_emoji(885592462599536701)))
            else:
                if guild_id not in ignored.guildkeys():
                    ignored.addguild(guild_id)
                if member.id not in ignored.guilds[guild_id]:
                    if member.id == my_id:
                        ignoreable.pop(ignoreable.members.index(ctx.author.id))
                        await ctx.send("You tried to add my owner in ignore list, instead now you've lost your owner position {}".format(get_emoji(893546552864411738)))
                    else:
                        if member.id == ctx.author.id:
                            await ctx.send("You can't add yourself in `ignore list` dumbass {}".format(get_emoji(892480880810020896)))
                        elif member.id in ignoreable.members:
                            await ctx.send(f"{member.mention} is an `ignore cmd owner`, can't add him/her in ignore list {get_emoji(890869939429314610)}")
                        else:
                            ignored.guilds[guild_id].append(member.id)
                            await ctx.send(f"Not responding to {member.mention}'s commands other than `help` until unignored {get_emoji(random.choice([876025887039049738, 892776197887524935, 775397275886813226]))}")
                else:
                    await ctx.send(f'{member.mention} is already in my dump list {get_emoji(random.choice([890869939429314610, 893546552864411738]))}')
                    return

@bot.command()
async def unignore(ctx, member:discord.Member=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())

    else:
        guild_id = ctx.guild.id
        if guild_id not in ignored.guildkeys():
            ignored.addguild(guild_id)
        if ctx.author.id not in ignoreable.members:
            return
        else:
            if member == None:
                await ctx.send('Mention a user to unignore {}'.format(get_emoji(885592462599536701)))
            else:
                if member.id in ignored.guilds[guild_id]:
                    index = ignored.guilds[guild_id].index(member.id)
                    ignored.guilds[guild_id].pop(index)
                    await ctx.send('Removed {} from dump list {}'.format(member.mention, get_emoji(random.choice([876032718486507591, 892776197887524935]))))

@bot.command(aliases=['clearil'])
async def clearignorelist(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())

    else:
        if ctx.author.id not in ignoreable.members:
            return
        else:
            guild_id = ctx.guild.id
            if guild_id not in ignored.guildkeys():
                ignored.addguild(guild_id)
            ignored.guilds[guild_id] = []
            await ctx.send('Ignored members list is cleared {}'.format('✅')) 

@bot.command()
async def ping(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())
        
    else:
        guild_id = ctx.guild.id
        if guild_id not in ignored.guilds:
            ignored.addguild(guild_id)
        if ctx.author.id in ignored.guilds[guild_id]:
            return
        else:
            await ctx.send(f"Pong! {round(bot.latency*1000, 1)}ms")

def insta_embed(dialouge=None):
    embed = discord.Embed(description=f"```py\n{dialouge}```", color=0xe30eae).set_footer(text="Enjoy")
    return embed

@bot.command()
async def insta(ctx, url:str=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())

    else:
        guild_id = ctx.guild.id
        if guild_id not in ignored.guilds:
            ignored.addguild(guild_id)
        if ctx.author.id in ignored.guilds[guild_id]:
            return
        else:
            if url == None:
                await ctx.send(f'Provide a URL {get_emoji(885592462599536701)}')
            else:
                message = await ctx.send('Checking the URL')
                if url.startswith('https://www.instagram.com/') == False:
                    await message.edit(content=f'The URL which was specified was either not a insta URL or an unexpected URL or maybe {get_emoji(774297843094782013)}')
                elif 'audio' in url:
                    await message.edit(content=f"I don't process audio...for now that is {get_emoji(921055619199422485)}")
                else:
                    await message.edit(content=f'{get_emoji(892750347599233034)} Processing your request, this may take some time.....')
                    try:
                        api = 'https://instaapi.glitch.me/allinone'

                        headers = {'url' : url}

                        response = requests.get(url=api, headers=headers).json()
                    except:
                        await message.edit(content="The request was not fullfilled for some reason.")
                        return
                    try:
                        post_url = response['video']
                        embed = insta_embed(dialouge="Here's the Download button for the video you searched for✅")
                        buttons = [
                            create_button(label='Download', style=ButtonStyle.URL, url=await shorten_url(post_url[0]))
                        ]
                        action_row = create_actionrow(*buttons)
                        await message.delete()
                        await ctx.send(embed=embed, components=[action_row])
                    except:
                        try:
                            post_url = response['image']
                            embed = insta_embed(dialouge="Here's the Download button for the image you searched for✅")
                            await message.delete()
                            await ctx.send(embed=embed, components=[action_row])
                        except:
                            await message.edit(content=f"Couldn't fetch the requsted video, please invoke the command again and try {get_emoji(928317890208333955)}")

async def get_channel_info(url):
    results = YoutubeSearch(search_terms=url, max_results=1).to_dict()
    if len(results) == 0:
        return None
    return results[0]

def yt_embed(channel_info, dialouge=None):
    embed = discord.Embed(
                        title=title, 
                        description=f'```py\nName: {title}\n\nViews: {channel_info["views"][0:-6]}\n\n\n{dialouge}```',
                        color=discord.Color.red()
             ).set_thumbnail(url=f"https://img.youtube.com/vi/{vid_id}/hqdefault.jpg").set_footer(text="By {}".format(channel_info['channel']))
    return embed

def vid_dict_maker(vids_dict):
    new_dict = {}
    index = 1
    for key in vids_dict:
        in_dict = vids_dict[key]
        new_dict.update({index :{'quality': in_dict['q'], 'size' : in_dict['size'], 'ftype' : in_dict['f']}})
        index += 1

    return new_dict

async def retry(info):
    channel = bot.get_channel(error_channel_id)
    embed = discord.Embed(title="Alert from YT command", description='The command invoked `retry` block to process a video', color=color())
    await channel.send(embed=embed)
    for i in range(1, 4):
        response = requests.post(url='https://yt1s.io/api/ajaxSearch', data={'q' : info['url'], 'vt' : 'home'}).json()
        f_name = response['fn']
        data = {
                'v_id' : response['vid'], 
                'ftype' : info['ftype'], 
                'fquality' : info['fquality'], 
                'token' : response['token'],
                'timeExpire' : response['timeExpires'],
                'client' : 'yt1s.io'
            }
        response = requests.post(url='https://backend.svcenter.xyz/api/convert-by-45fc4be8916916ba3b8d61dd6e0d6994', headers=headers, data=data).json()
        server_url = response['c_server']
        data.pop('client')
        data.update({'fname' : f_name})
        final_response = requests.post(url=server_url+'/api/json/convert', data=data).json()
        try:
            buttons = [
                create_button(label='Download', style=ButtonStyle.URL, url=await shorten_url(final_response['result']))
            ]
            action_row = create_actionrow(*buttons)
            embed = yt_embed(channel_info=info['channel-info'], dialouge="Here's the Download button for the video you searched for✅")
            await info['message'].edit(embed=embed, components=[action_row])
            embed.description = "The `retry` block responded with a valid **URl**✅ in the {}'s try".format(i)
            await channel.send(embed=embed)
            return 'Lmao'
        except:
            pass
    embed.description = "The `retry` block couldn't respond with a valid URL :("
    await channel.send(embed=embed)
    return None

@slash.slash(
    name='youtube',
    description='Choose the file format and quality of a YT video which you desire to download',
    guild_ids=all_guilds,
    options=[
        create_option(
            name='url', 
            description='URL of the video',
            required=True,
            option_type=3
        )
    ]
)
@bot.command()
async def yt(ctx, url:str=None):

    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())
        
    else:
        guild_id = ctx.guild.id
        if guild_id not in ignored.guilds:
            ignored.addguild(guild_id)
        if ctx.author.id in ignored.guilds[guild_id]:
            return
        else:
            if url is None:
                await ctx.send("Give a URL of the video you want to download.")

            else:
                message = await ctx.send('Checking the URL...')
                if url.startswith('https://youtu.be/') == False and url.startswith('https://youtube.com/shorts/') == False and url.startswith('https://www.youtube.com/') == False:
                    await message.edit(content='Invalid url for this command.')
                    return   
                else:
                    await message.edit(content='Fetching all the available formats of the video....')
                    try:
                        api = "https://yt1s.io/api/ajaxSearch"
                        data = {'q' : url, 'vt' : 'home'}
                        response = requests.post(api, data=data).json()
                        global vid_id, title
                        vid_id = response['vid']
                        title = response['title']
                        videos_dict = vid_dict_maker(response['links']['mp4'])
                        channel_info = await get_channel_info(url=url)
                        embed = yt_embed(channel_info=channel_info, dialouge="Pick a format for the file👇")
                        list = create_select(
                                options=[
                                    create_select_option(label='1. Mp4 (Video)', value='1'),
                                    create_select_option(label='2. Mp3 (Audio)', value='2')
                                ],
                                placeholder='Choose the format',
                                max_values=1,
                                min_values=1
                            )
                        action_row = create_actionrow(list)
                        await message.edit(embed=embed, content="", components=[action_row])
                        def check(action):
                            return action.author_id == ctx.author.id

                        try:
                            format_req_ctx: ComponentContext = await wait_for_component(client=bot, components=action_row,check=check, timeout=20)
                            choice = int(format_req_ctx.values[0])
                        except asyncio.TimeoutError:
                            await message.delete()
                            await ctx.send('You failed to respond in time')
                            return

                        if choice == 1:
                            list = create_select(
                                options=yt_quality_options(dict=videos_dict),
                                placeholder='Available Qualities',
                                min_values=1,
                                max_values=1
                            )
                            embed = yt_embed(channel_info=channel_info, dialouge='Choose the quality of the video you desire to download')
                            action_row = create_actionrow(list)
                            await format_req_ctx.edit_origin(components=[action_row], embed=embed)
                            try:
                                quality_req_ctx: ComponentContext = await wait_for_component(client=bot, components=action_row, check=check, timeout=20)
                                embed = yt_embed(channel_info=channel_info, dialouge="Processing your yt video with the desired quality...")
                                await quality_req_ctx.edit_origin(embed=embed, components=[])
                            except asyncio.TimeoutError:
                                await message.delete()
                                await ctx.send('You failed to respond in time')
                                return
                            index = int(quality_req_ctx.values[0])
                            data = {
                                'v_id' : vid_id, 
                                'ftype' : videos_dict[index]['ftype'], 
                                'fquality' : videos_dict[index]['quality'], 
                                'token' : response['token'],
                                'timeExpire' : response['timeExpires'],
                                'client' : 'yt1s.io'
                            }
                            global headers
                            headers = {'x-requested-key' : 'de0cfuirtgf67a'}
                            f_name = response['fn']
                            try:
                                response = requests.post(url='https://backend.svcenter.xyz/api/convert-by-45fc4be8916916ba3b8d61dd6e0d6994', headers=headers, data=data).json()
                                server_url = response['c_server']
                                data.pop('client')
                                data.update({'fname' : f_name})

                                final_response = requests.post(url=server_url+'/api/json/convert', data=data).json()
                                buttons = [
                                    create_button(label='Download', style=ButtonStyle.URL, url=await shorten_url(final_response['result']))
                                ]
                                action_row = create_actionrow(*buttons)
                                embed = yt_embed(channel_info=channel_info, dialouge="Here's the Download button for the video you searched for✅")
                                await message.edit(embed=embed, components=[action_row])
                            except Exception as e: 
                                result = await retry(info={'ctx' : ctx, 'url' : url, 'message' : message,'channel-info' : channel_info,'ftype' : videos_dict[index]['ftype'], 'fquality' : videos_dict[index]['quality']})
                                if result == None:
                                    embed = discord.Embed(description='An error occured while parsing the url, please use the command again and on the account of meeting the issue again, try the cmd with a lower quality.\nSorry for inconvinience.', color=0xe80e32)
                                    await message.edit(embed=embed)
                                    channel = bot.get_channel(error_channel_id)
                                    embed = discord.Embed(title='Error raised in '+str(ctx.command), description=e, color=color())
                                    await channel.send(embed=embed)
                        elif choice == 2:
                            YTDL_OPTIONS = {'format' : 'bestaudio', 'cookiefile' : './cookie.txt'}
                            with YoutubeDL(YTDL_OPTIONS) as ytdl:
                                info = ytdl.extract_info(url, download=False)
                            d_link = info['formats'][0]['url']
                            buttons = [
                                create_button(label='Download', style=ButtonStyle.URL, url=await shorten_url(url=d_link))
                            ]
                            action_row = create_actionrow(*buttons)
                            await format_req_ctx.edit_origin(content="", components=[action_row], embed=embed)
                    except Exception as e:
                        await message.edit(content="Kuch error aya hai, mere owner ko gaali de", embed=None, components=[])
                        channel = bot.get_channel(error_channel_id)
                        embed = discord.Embed(title='Error raised in '+str(ctx.command), description=e, color=color())
                        await channel.send(embed=embed)

@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command()
async def spam(ctx, member:discord.Member=None, *, message=""):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())
        
    else:
        guild_id = ctx.guild.id
        if guild_id not in ignored.guilds:
            ignored.addguild(guild_id)
        if ctx.author.id in ignored.guilds[guild_id]:
            return
        else:
            if member.id != winsy_id:
                for msg in range(10):
                    await ctx.send(f'{member.mention} {message}')

            else:
                await ctx.send(random.choice(['How foolish of you to make me spam myself.', "I don't have time to listen to your shitty request.", "Go study, atleast that'll prove to be usefull"]))

@spam.error
async def command_name_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(description=f"**{ctx.author.mention} Slow it down bro!**\n\nYou are under Cooldown, you can spam after {error.retry_after:.2f}sec", color=color())
        await ctx.send(embed=embed)

@bot.command()
@has_permissions(kick_members=True)
async def kick(ctx, member:discord.Member=None, *,reason:str=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())
        
    else:
        if member is None:
            await ctx.send("Mention a user to kick")
        elif reason is None:
            await ctx.send("You need to provide a reason to kick someone")
        elif member.id == my_id or member.id == chizu_id:
            await ctx.send(f"Can't kick {member.mention} as they are one of the VIPs {get_emoji(881253669083955221)}")
            
        else:
            await ctx.send(f"{ctx.author.mention} Do you confirm to kick {member.mention} from this server?\nReply with yes/y or no/n")

            def check(m):
                return m.author.id == ctx.author.id and m.channel == ctx.message.channel and m.content.lower() in ["yes", "y", "no", "n"]

            try:
                reply = await bot.wait_for('message', check=check, timeout=20)
            except asyncio.TimeoutError:
                await ctx.send(embed=Embeds.command_cancelled())
                return
            if reply.content.lower() in ["yes", "y"]:
                await member.kick(reason=reason)
                await ctx.send(f"Kicked Successfully {get_emoji(885592612692709406)}")
            else:
                await ctx.send(embed=Embeds.command_cancelled())

@bot.command()
async def mute(ctx, member:discord.Member=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())
        
    else:
        if ctx.author.id == ctx.guild.owner_id or ctx.author.id == my_id:
            if member is None:
                await ctx.send("Mention a user to mute")
            else:
                role = discord.utils.get(ctx.guild.roles, name='mute')
                if role is None:
                    role = discord.utils.get(ctx.guild.roles, name='muted')
                    if role is None:
                        embed = discord.Embed(description='Found no mute roles in the server')
                        await ctx.send(embed=embed)
                    else:
                        await member.add_roles(role)
                        await ctx.send(f"Muted {member.mention} {get_emoji(774296198211043329)}")
                else:
                    await member.add_roles(role)
                    await ctx.send(f"Muted {member.mention} {get_emoji(774296198211043329)}")
        else:
            await ctx.send("You're missing permissions to use this command.")

@bot.command()
async def unmute(ctx, member:discord.Member=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())
        
    else:
        if ctx.author.id == ctx.guild.owner_id or ctx.author.id == my_id:
            if member is None:
                await ctx.send("Mention a user to unmute")
            else:
                role = discord.utils.get(member.roles, name='mute')
                if role is None:
                    role = discord.utils.get(member.roles, name='muted')
                    if role is None:
                        await ctx.send(f"{member.mention} is not muted {get_emoji(876025069866999808)}")
                    else:
                        await member.remove_roles(role)
                        await ctx.send(f"Unmuted {member.mention} {get_emoji(random.choice([775398330150813736, 876032718486507591, 894576946321694751, 876025887039049738]))}")
                else:
                    await member.remove_roles(role)
                    await ctx.send(f"Unmuted {member.mention} {get_emoji(random.choice([775398330150813736, 876032718486507591, 894576946321694751, 876025887039049738]))}")
        else:
            await ctx.send("You're missing permissions to use this command.")

@bot.command()
@has_permissions(manage_roles=True)
async def purge(ctx, amount:int=None, slash=False):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())
        
    else:
        guild_id = ctx.guild.id
        if guild_id not in ignored.guilds:
            ignored.addguild(guild_id)
        if ctx.author.id in ignored.guilds[guild_id]:
            return
        else:
            if slash:
                await ctx.channel.purge(limit=amount)
                await ctx.send("Successfully purged {} messages".format(amount), hidden=True)
            else:
                if amount == None:
                    await ctx.send("Mention the amount of messages you want to purge")
                else:
                    await ctx.channel.purge(limit=amount+1)
                    await ctx.send("Successfully purged {} messages".format(amount), hidden=True)

class Atlas:
    
    Players = {}
    Used_places = {}
    End = {}

    def fetch_places():
        places = []
        cursor = conn.cursor()
        data = cursor.execute("""SELECT * FROM Atlas""").fetchall()
        for tup in data:
            places.append(tup[-1])
        return places

    def __init__(self, member:discord.Member):
        self.name = str(member)
        self.id = member.id
        self.mention = member.mention
        self.lifes = 3
        self.points = 0

    def __repr__(self):
        return self.name
    
    def Register_Server(ctx):
        Atlas.Used_places.update({ctx.guild.id : []})

    async def increase_point(self, msg):
        self.points += 1
        await msg.reply(f"Correct Answer!!✅\nTotal Points: {self.points}")
        if self.points == 10:
            await self.won(msg)

    async def already_used(self, msg, place):
        await self.cut_life(msg, reason=f'used {place}')
    
    async def cut_life(self, msg, reason:str):
        self.lifes -= 1
        if reason == 'incorrect':
            if self.lifes == 0:
                await msg.reply("Incorrect response")
                await self.eliminate(msg)
            else:
                await msg.reply(f"Incorrect response, life decreased by 1\nTotal lifes left **{self.lifes}**")
        elif reason == 'timeout':
            if self.lifes == 0:
                await msg.channel.send(f"{self.mention}You failed to respond within time")
                await self.eliminate(msg)
            else:
                await msg.send(f"{self.mention} You failed to respond within time, life decreased by 1\nTotal lifes ")
        elif reason.startswith('used'):
            if self.lifes == 0:
                await msg.reply(f"***{reason[5:]}*** is already used by someone")
                await self.eliminate(msg)
            else:
                await msg.reply(f"***{reason[5:]}*** is already used by someone, you can't use it again, life decreased by 1")

    async def eliminate(self, msg):
        Atlas.Players[msg.guild.id].pop(Atlas.Players[msg.guild.id].index(self))
        await msg.channel.send(f"{self.mention} You're eliminated from the game.")
        if len(Atlas.Players[msg.guild.id]) == 1:
            await Atlas.won(msg, Atlas.Players[msg.guild.id][0])
    
    def used(ctx, place):
        Atlas.Used_places[ctx.guild.id].append(place.lower())

    def jumble(ctx):
        indexes = []
        jumbled = []
        spacer = 0
        for i in range(len(Atlas.Players[ctx.guild.id])):
            jumbled.append(None)
            indexes.append(spacer)
            spacer += 1
        for player in Atlas.Players[ctx.guild.id]:
            index = random.choice(indexes)
            jumbled[index] = player
            indexes.pop(indexes.index(index))

        Atlas.Players[ctx.guild.id] = jumbled

    def valid_place(place:str):
        places = Atlas.fetch_places()
        if place.lower() in places:
            return True
        else:
            possible_correction = SpellChecker().correction(place)
            if possible_correction.lower() in places:
                return True
            else:
                return False

    async def start(ctx):
        Player = Atlas.Players[ctx.guild.id][0]
        await ctx.send(f"{Player.mention} It's your turn, start the game by giving a name of a country or capital")
        def check(m):
            return m.channel.id == ctx.channel.id and m.author.id == Player.id
        try:
            response = await bot.wait_for('message', check=check, timeout=10)
            return [Player, response]
        except asyncio.TimeoutError:
            return [Player, None]

    async def ask(self, ctx, last_letter:str):
        await ctx.send(f"{self.mention} Give a name of a country or a capital by the starting letter of ***{last_letter.upper()}***")
        def check(m):
            return m.channel.id == ctx.channel.id and m.author.id == self.id
        try:
            response = await bot.wait_for('message', check=check, timeout=10)
            return response
        except asyncio.TimeoutError:
            return None

    async def won(msg, Player):
        Atlas.End[msg.guild.id] = True
        await msg.channel.send(f"{Player.mention} You've won the game!!")

    async def correct_response(self, ctx):
        await self.increase_point(ctx)

    async def wrong_response(self, ctx):
        await self.cut_life(ctx, reason='incorrect')

    async def timeout(self, msg):
        await self.cut_life(msg, reason='timeout')
    
    def Clear_game(ctx):
        Atlas.Players.pop(ctx.guild.id)
        Atlas.Used_places.pop(ctx.guild.id)
        Atlas.End.pop(ctx.guild.id)

@bot.command()
async def atlas(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())

    else:
        guild_id = ctx.guild.id
        if guild_id not in ignored.guilds:
            ignored.addguild(guild_id)
        if ctx.author.id in ignored.guilds[guild_id]:
            return
        else:
            if ctx.guild.id in Atlas.Players.keys():
                await ctx.send("Can't initiate another ***Atlas game*** as a game is already in play in this server.")
            else:
                Atlas.End.update({ctx.guild.id : False})
                embed = discord.Embed(title=f'**Atlas**', description='react on this message with the check to participate ✅')
                embed.set_footer(icon_url='https://cdn.discordapp.com/emojis/892751786719469598.gif?size=56', text='Good luck')
                message = await ctx.send(embed=embed)
                await message.add_reaction('✅')
            
                await asyncio.sleep(5)

                await ctx.send('Registration closed')

                cached_msg = discord.utils.get(bot.cached_messages, id=message.id)
                Atlas.Players.update({ctx.guild.id : []})
                for reaction in cached_msg.reactions:
                    if reaction.emoji == '✅':
                        users = await reaction.users().flatten()
                        for user in users:
                            if user.id != winsy_id:
                                Atlas.Players[ctx.guild.id].append(Atlas(user))
                if Atlas.End[ctx.guild.id] == False:
                    Atlas.jumble(ctx)

                    if Atlas.Players[ctx.guild.id] == []:
                        Atlas.Players.pop(ctx.guild.id)
                        await ctx.send('No players reacted, the game is terminated.')
                        
                    elif len(Atlas.Players[ctx.guild.id]) < 2:
                        Atlas.Players.pop(ctx.guild.id)
                        await ctx.send('Atleast 2 players are needed to start the game.')

                    else:
                        if Atlas.End[ctx.guild.id] == False:
                            Atlas.Register_Server(ctx)
                            await ctx.send('Game starts now!!')
                            
                            Last_letter = None
                            first_response = await Atlas.start(ctx)
                            if Atlas.End[ctx.guild.id] == False:
                                if first_response[1] is not None:
                                    if Atlas.valid_place(first_response[1].content):
                                        Atlas.used(ctx, first_response[1].content)
                                        await first_response[0].correct_response(first_response[1])
                                        Last_letter = first_response[1].content[-1]
                                    else:
                                        await first_response[0].wrong_response(first_response[1])
                                else:
                                    await first_response[0].timeout(ctx)

                                Pointer = 1
                                if Last_letter == None:
                                    Last_letter = random.choice("A B C D E F G H I J K L M N O P Q R S T U V W X Y Z".split(" "))

                                while True:
                                    if Atlas.End[ctx.guild.id] == False:
                                        if Pointer == len(Atlas.Players[ctx.guild.id]):
                                            Pointer = 0
                                        
                                        Current_player: Atlas = Atlas.Players[ctx.guild.id][Pointer]
                                        Response = await Current_player.ask(ctx, last_letter=Last_letter)
                                        if Response != None:
                                            if Response.content.lower() in Atlas.Used_places[ctx.guild.id]:
                                                await Current_player.already_used(Response, Response.content)
                                            elif Atlas.valid_place(Response.content):
                                                Atlas.used(ctx, Response.content)
                                                Last_letter = Response.content[-1]
                                                await Current_player.correct_response(Response)
                                            else:
                                                await Current_player.wrong_response(Response)
                                        else:
                                            await Current_player.timeout(ctx)

                                        Pointer += 1
                                    else:
                                        try:
                                            Atlas.Clear_game(ctx)
                                        except:
                                            pass
                                        break

@bot.command()
async def stop_atlas(ctx):
    if ctx.guild.id in Atlas.Players.keys():
        player_ids = []
        for player in Atlas.Players[ctx.guild.id]:
            player_ids.append(player.id)
        if ctx.author.id in player_ids:
            Atlas.End[ctx.guild.id] = True
            Atlas.Clear_game(ctx)
            await ctx.reply("Game has been stopped {}".format(get_emoji(random.choice([775398330150813736, 892776197887524935]))))
    else:
        await ctx.reply("There's no game running in this server currently")

@bot.command()
async def laugh(ctx, at, member:discord.Member=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())
        
    else:
        guild_id = ctx.guild.id
        if guild_id not in ignored.guilds:
            ignored.addguild(guild_id)
        if ctx.author.id in ignored.guilds[guild_id]:
            return
        else:
            if at == "at" or at == "At" or at == "aT" or at == "AT":
                if member is None:
                    await ctx.send("Mention a user to laugh at")
                
                else:
                    if member.id == winsy_id:
                        await ctx.send("How foolish of you to make me laugh at myself")

                    else:
                        choice_gif = random.choice(laugh_command_gifs)
                        embed = discord.Embed(description=member.mention, colour=color())
                        embed.set_image(url=choice_gif)
                        await ctx.send(embed=embed)

            else:
                return

@bot.command(aliases=["gn", "oyasumi", "Oyasumi", "Gn"])
async def goodnight(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())
        
    else:
        guild_id = ctx.guild.id
        if guild_id not in ignored.guilds:
            ignored.addguild(guild_id)
        if ctx.author.id in ignored.guilds[guild_id]:
            return
        else:
            choice = random.choice(good_night_replies)
            choice_gif = random.choice(good_night_gifs)
            embed = discord.Embed(description=f"**{choice}** {ctx.author.mention}", colour=color())
            embed.set_image(url=choice_gif)
            await ctx.send(embed=embed) 

@bot.command()
async def brofist(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())
        
    else:
        guild_id = ctx.guild.id
        if guild_id not in ignored.guilds:
            ignored.addguild(guild_id)
        if ctx.author.id in ignored.guilds[guild_id]:
            return
        else:
            file = discord.File(f"Winsy_/bro_fist/e4579003-ac2f-478d-874e-da4ad0f25cf0.jpg")
            embed = discord.Embed(description=f"**{random.choice(bro_fist_replies)}** {ctx.author.mention}", colour=color())
            embed.set_image(url=f"attachment://e4579003-ac2f-478d-874e-da4ad0f25cf0.jpg")
            await ctx.send(file=file, embed=embed)

@bot.command(aliases=["gay"])
async def gae(ctx, member:discord.Member=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())
        
    else:
        guild_id = ctx.guild.id
        if guild_id not in ignored.guilds:
            ignored.addguild(guild_id)
        if ctx.author.id in ignored.guilds[guild_id]:
            return
        else:
            if member == None:
                await ctx.send("You need to mention a user to use this command")
            else:
                embed = discord.Embed(title=f":rainbow_flag: Gae %", colour=color())
                cant_gay_you = ["I can't gay you Yosh", "Why u wanna gay yourself senpai Yosh •_•"]
                dont_gay_me = ["Why u wanna gay me master ༎ຶ‿༎ຶ", "Please don't gay me senpai ಥ‿ಥ"]
                if ctx.author.id == my_id:
                    if member.id == my_id:
                        await ctx.send(random.choice(cant_gay_you))
                    elif member.id == winsy_id:
                        await ctx.send(random.choice(dont_gay_me))
                    else:
                        embed.description=f"{member.name} is {random.randint(0, 101)}% gae"
                        await ctx.send(embed=embed)
                elif member.id == my_id:
                    embed.description = f"{member.name} is 0% gae and 100% chad, Although {ctx.author.name} is probably {random.randint(90, 101)}% gae"
                    await ctx.send(embed=embed)
                elif member.id == winsy_id:
                    reply = "I decide who is gae, and I can't be the one to be gayed bruh"
                    await ctx.send(reply)
                else:
                    embed.description=f"{member.name} is {random.randint(0, 101)}% gae"
                    await ctx.send(embed=embed)

@bot.command()
async def roast(ctx, member:discord.Member=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())
        
    else:
        guild_id = ctx.guild.id
        if guild_id not in ignored.guilds:
            ignored.addguild(guild_id)
        if ctx.author.id in ignored.guilds[guild_id]:
            return
        else:
            if member == None:
                await ctx.send("You need to mention a user to roast")
            else:
                if member.id == winsy_id:
                    kiralaugh = get_emoji(892772725343535104)
                    emoji = get_emoji(random.choice([890869939429314610, 892480880810020896, 892751786719469598, 885592612692709406]))
                    dialouge = ""
                    if emoji.id == 892751786719469598 or emoji.id == 885592612692709406:
                        dialouge += random.choice(["Take this instead", "Not roast, take booty"])

                    elif emoji.id == 890869939429314610:
                        await ctx.message.reply(f"{dialouge}{emoji}")
                        await asyncio.sleep(2)
                        await ctx.send(f"{kiralaugh}")
                        return

                    await ctx.reply(f"{dialouge}{emoji}")

                else:
                    dict = await fetch_roasts(member.id)
                    roasts = dict.get('roasts')
                    type = dict.get('type')
                    roast_choice = random.choice(roasts)
                    if type == 'Normal':
                        await ctx.send(f"{member.mention} {roast_choice}")

                    else:
                        await ctx.reply(roast_choice)

@bot.command()
async def why(ctx, insult:str=None, member:discord.Member=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())
        
    else:
        guild_id = ctx.guild.id
        if guild_id not in ignored.guilds:
            ignored.addguild(guild_id)
        if ctx.author.id in ignored.guilds[guild_id]:
            return
        else:
            if insult.lower() == 'insult':
                if member is not None:
                    await ctx.send(f"{member.mention} I'm not insulting you. I'm describing you.")
                else:
                    await ctx.send(f"{ctx.author.mention} I'm not insulting you. I'm describing you.")
            
            else:
                return

async def fetch_king_data():
    cursor = conn.cursor()
    data = cursor.execute("""SELECT * FROM king_cmd""").fetchall()
    one = random.choice(data)
    dict = {'image' : one[0], 'button' : one[1], 'response' : one[2], 'button_type' : one[3]}
    return dict

@slash.slash(
    name='you_dropped_this',
    description='👑',
    guild_ids=all_guilds,
    options=[
        create_option(
            name='user',
            description="Who's the king? 👑",
            required=True,
            option_type=6
        )
    ]
)
async def king(ctx: SlashContext, user: discord.Member):
    opt = await fetch_king_data()
    embed = discord.Embed(description=user.mention)
    embed.set_image(url=opt['image'])
    if opt['button_type'] == 'custom':
        opt['button'] = get_emoji(opt['button'])
        buttons = [
            create_button(style=ButtonStyle.grey, label='TAKE IT👉👉', disabled=True),
            create_button(style=ButtonStyle.blue, emoji=opt['button']),
            create_button(style=ButtonStyle.grey, label='👈👈TAKE IT', disabled=True)
        ]
    else:
        buttons = [
            create_button(style=ButtonStyle.grey, label='TAKE IT👉👉', disabled=True),
            create_button(style=ButtonStyle.blue, label=opt['button']),
            create_button(style=ButtonStyle.grey, label='👈👈TAKE IT', disabled=True)
        ]
    action_row = create_actionrow(*buttons)
    lol = await ctx.send(embed=embed, components=[action_row])
    def check(component_ctx: ComponentContext):
        return component_ctx.author_id == user.id
    try:
        button_ctx = await wait_for_component(bot, components=action_row, timeout=20, check=check)
        if button_ctx.component['label'] == opt['button']:
            await button_ctx.edit_origin(content=opt['response'], components=[], embed=None)
    except asyncio.TimeoutError:
        await lol.edit(content=f"{user.mention} Maybe you didn't deserve it {get_emoji(921055619199422485)}", components=[], embed=None)

# @bot.event
# async def on_command_error(ctx, error):
#     channel = bot.get_channel(error_channel_id)
#     embed = discord.Embed(title='Error raised in '+str(ctx.command), description=error, color=color())
#     await channel.send(embed=embed)

@bot.command()
async def servers(ctx):
    cursor = conn.cursor()
    data = cursor.execute("""SELECT * FROM My_Guilds""").fetchall()
    servers = ""
    ctr = 1
    for server in data:
        servers += f"{ctr}. {server[0]}\n"
        ctr += 1
    embed = discord.Embed(title='All the registered servers are', description=servers, color=color())
    await ctx.reply(embed=embed)

all_cogs = os.listdir('./Winsy_/cogs')
for file in all_cogs:
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')