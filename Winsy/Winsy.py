from datetime import time
import sqlite3
import discord
import random
import asyncio
import os
import bitly_api
from discord.enums import try_enum
import requests
from spellchecker import SpellChecker
from youtube_dl import YoutubeDL
from discord.ext import commands
from discord.ext.commands import has_permissions

bot = commands.Bot(command_prefix=commands.when_mentioned_or("T ", "t "))
bot.remove_command('help')

conn = sqlite3.connect("Winsy.db")

my_id = 762372102204030986
winsy_id = 873504810278739988

my_server_id = 762380604058632222

error_channel_id = 887385480679788574

bro_fist_replies = ["**Yesss boss!**", "**BRO FIST!!!**", "**Zhong Zhong**"]
good_night_replies = ["**Oyasumi!**", "**Night!**", "**Have a great night**", "**Sweet dreams**"]

good_night_gifs = ["https://c.tenor.com/3fAZZncIHDQAAAAC/smile-anime.gif", "https://c.tenor.com/ouo5podnrgUAAAAS/cuddle-love.gif", "https://c.tenor.com/01cElrH1Ed8AAAAS/anime-shiro.gif", "https://c.tenor.com/Bn_E6t9-m_wAAAAC/sleeping-kiss.gif", "https://c.tenor.com/3eouI6QChiEAAAAC/anime-cuteness.gif", "https://c.tenor.com/tVBrvOB5ttkAAAAC/11-sad.gif"]
laugh_command_gifs = ["https://cdn.discordapp.com/attachments/873552851157254144/874619767749758986/hehe.gif", "https://c.tenor.com/fqRNsILmXHQAAAAC/anime-girl.gif", "https://cdn.discordapp.com/attachments/873552851157254144/874620123930038282/natsu-lol.gif", "https://c.tenor.com/qEfogXAprQoAAAAC/nichijou-laughing.gif", "https://c.tenor.com/fbWCY-1exTsAAAAS/bokura-wa-minna-kawaisou-gifs-to-reaction.gif"]

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

@bot.event
async def on_ready():
    global my_guild
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
        embed.add_field(name="`spam <number of times> <user mention> <message(if any)>`", value="*Spams the message along with the mentioned user*", inline=False)
        embed.add_field(name="`poop at <user mention>`", value="*Poops in the dm of the mentioned user*", inline=True)
        await ctx.send(embed=embed)
        await ctx.message.delete()

    elif category == '2':
        embed = discord.Embed(title="**Interactive commands**", description="All the commands to interact with the bot.", color=color())
        embed.add_field(name="`goodnight` Possible aliase(s): `gn`, `oyasumi` ", value="*Winsy wishes goodnight*", inline=False)
        embed.add_field(name="`laugh at <user>`", value="*Winsy laughs at the mentioned user*", inline=False)
        embed.add_field(name="`brofist`", value="*Winsy wishes **brofist***", inline=False)
        embed.add_field(name="`why insult <user>`", value="*Winsy explains the reason to laugh at the <user>*", inline=False)
        await ctx.send(embed=embed)
        await ctx.message.delete()

    elif category == '3':
        embed = discord.Embed(title="**Search commands**", description="All the search commands", color=color())
        embed.add_field(name="`insta <insta post/reel link>`", value="Sends the media link for the user to download", inline=False)
        embed.add_field(name='`yt <vid link>`', value="Sends the media link for the user to download", inline=False)
        await ctx.send(embed=embed)
        await ctx.message.delete()

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
                if url.startswith('https://www.instagram.com/p') == False and url.startswith('https://www.instagram.com/reel') == False and url.startswith('https://www.instagram.com/tv') == False:
                    await message.edit(content=f'The URL which was specified was either not a insta URL or an unexpected URL or maybe {get_emoji(774297843094782013)}')
                else:
                    await message.edit(content=f'{get_emoji(892750347599233034)} Processing your request, this may take some time.....')
                    try:
                        api = 'https://dl.instavideosave.com/allinone'

                        headers = {'url' : url}

                        response = requests.get(url=api, headers=headers).json()
                    except:
                        await message.edit(content="The request was not fullfilled for some reason.")
                        return
                    try:
                        post_url = response['video']
                        embed = await embed_maker(link=await shorten_url(post_url[0])+'video')
                        await message.delete()
                        await ctx.send(embed=embed) 
                    except:
                        try:
                            post_url = response['image']
                            embed = await embed_maker(link=await shorten_url(post_url[0])+'image')
                            await message.delete()
                            await ctx.send(embed=embed)
                        except:
                            await message.edit(content=f"The post is either from a private account or invalid url {get_emoji(885592462599536701)}")

@bot.command()
async def yt(ctx, url:str=None):

    def vid_dict_maker(vids_dict):
        new_dict = {}
        index = 1
        for key in vids_dict:
            in_dict = vids_dict[key]
            if in_dict['q'] != 'auto':
                value = {index :{'quality': in_dict['q'], 'size' : in_dict['size'], 'url' : in_dict['k']}}
                new_dict.update(value)
                index += 1

        return new_dict

    def fetch_key(dict):
        for i in dict:
            return i

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
                if url.startswith('https://youtu.be/') == False and url.startswith('https://youtube.com/shorts/') == False:
                    await message.edit(content='Invalid url for this command.')
                    return   
                else:
                    await message.edit(content='Fetching all the available formats of the video....')
                try:
                    api = "https://yt1s.com/api/ajaxSearch/index"
                    data = {'q' : url, 'vt' : 'home'}
                    response = requests.post(api, data=data).json()
                    audios_key_dict = response['links']['mp3']
                    audios_dict = audios_key_dict[fetch_key(audios_key_dict)]
                    vid_id = response['vid']
                    videos_dict = vid_dict_maker(response['links']['mp4'])
                    embed = discord.Embed(description='In which format do you want to download the file:\n **1.** *Mp4(Video)*\n**2.** *Mp3(Audio)*')
                    await message.edit(embed=embed, content="")
                    def check1(m):
                        return m.author.id == ctx.author.id and m.channel == ctx.message.channel

                    try:
                        format_req = await bot.wait_for('message', check=check1, timeout=10)
                        choice = format_req.content
                    except asyncio.TimeoutError:
                        await message.delete()
                        await ctx.send('You failed to respond in time')
                        return
                    try:
                        int(choice)

                    except:
                        await ctx.send("Bro I'm asking for indexes here")
                        return
                    if choice != '1' and choice != '2':
                        await message.delete()
                        await ctx.send("Invalid index given")
                    else:
                        if choice == '1':
                            embed = await embed_maker(dict=videos_dict)
                            await format_req.delete()
                            await message.edit(embed=embed, content="")
                            def check2(m):
                                return m.author.id == ctx.author.id and m.channel == ctx.message.channel

                            try:
                                quality_req = await bot.wait_for('message', check=check2, timeout=10)

                            except asyncio.TimeoutError:
                                await message.delete()
                                await ctx.send('You failed to respond in time')
                                return

                            try:
                                index = int(quality_req.content)

                            except:
                                await message.delete()
                                await ctx.send("Bro I'm asking for indexes here.")
                                return
                            if index not in videos_dict:
                                await ctx.send('Invalid index given')
                            else:
                                await quality_req.delete()
                                await message.delete()
                                message_ = await ctx.send('Processing your yt video with the desired quality...')
                                req_url = videos_dict[index]['url']
                                data = {'vid' : vid_id, 'k' : req_url}
                                api = "https://yt1s.com/api/ajaxConvert/convert"
                                response = requests.post(api, data=data).json()
                                d_link = await shorten_url(response['dlink'])
                                embed = await embed_maker(link=d_link + 'video')
                                await message_.delete()
                                await ctx.send(embed=embed)
                        elif choice == '2':
                            await format_req.delete()
                            await message.delete()
                            YTDL_OPTIONS = {'format': 'bestaudio','cookiefile':'./cookie.txt'}
                            with YoutubeDL(YTDL_OPTIONS) as ytdl:
                                info = ytdl.extract_info(url, download=False)
                            d_link = await shorten_url(info['formats'][0]['url'])
                            embed = await embed_maker(link=d_link + 'audio')
                            await ctx.send(embed=embed)
                except:
                    await message.edit('Seems the like servers are down')

@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command()
async def spam(ctx, times=None, member:discord.Member=None, *, message=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())
        
    else:
        guild_id = ctx.guild.id
        if guild_id not in ignored.guilds:
            ignored.addguild(guild_id)
        if ctx.author.id in ignored.guilds[guild_id]:
            return
        else:
            try:
                int(times)
                if message is None:
                    if member.id != winsy_id:
                        if int(times) <= 10:
                            for msg in range(1, int(times)+1):
                                await ctx.send(f"{member.mention}")
                        else:
                            await ctx.send("Maximum spam limit is 10 times")

                    else:
                        await ctx.send(random.choice(['How foolish of you to make me spam myself.', "I don't have time to listen to your shitty request.", "Go study, atleast that'll prove to be usefull"]))
                else:
                    if member.id != winsy_id:
                        if int(times) <= 10:
                            for msg in range(1, int(times)+1):
                                await ctx.send(f"{member.mention} {message}")
                        else:
                            await ctx.send("Maximum spam limit is 10 times")

                    else:
                        await ctx.send(random.choice(['How foolish of you to make me spam myself.', "I don't have time to listen to your shitty request.", "Go study, atleast that'll prove to be usefull"]))

            except:
                await ctx.send("Use the command in this way `winsy spam <times> <user mention> <message(optional)>`")

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
@has_permissions(kick_members=True)
async def mute(ctx, member:discord.Member=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())
        
    else:
        if member is None:
            await ctx.send("Mention a user to mute")
        else:
            role = discord.utils.get(ctx.guild.roles, name='mute')
            if role is None:
                embed = discord.Embed(description="You need to make a 'mute' role in your server and set it's permissions to function accordingly")
                await ctx.send(embed=embed)
            else:
                await member.add_roles(role)
                await ctx.send(f"Muted {member.mention} {get_emoji(774296198211043329)}")

@bot.command()
@has_permissions(kick_members=True)
async def unmute(ctx, member:discord.Member=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())
        
    else:
        if member is None:
            await ctx.send("Mention a user to unmute")
        else:
            role = discord.utils.get(member.roles, name="mute")
            if role is None:
                await ctx.send(f"{member.mention} is not muted {get_emoji(876025069866999808)}")
            else:
                await member.remove_roles(role)
                await ctx.send(f"Unmuted {member.mention} {get_emoji(random.choice([775398330150813736, 876032718486507591, 894576946321694751, 876025887039049738]))}")

@bot.command()
@has_permissions(manage_roles=True)
async def purge(ctx, amount:int=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())
        
    else:
        guild_id = ctx.guild.id
        if guild_id not in ignored.guilds:
            ignored.addguild(guild_id)
        if ctx.author.id in ignored.guilds[guild_id]:
            return
        else:
            if amount == None:
                await ctx.send("Mention the amount of messages you want to purge")
            else:
                await ctx.channel.purge(limit=amount+1)

class Atlas:
    
    Players = []
    current_player = None
    Used_places = []
    End = False
    def fetch_countries():
        with open('./Winsy/Atlas.txt', 'r') as file:
            all = file.read()
        countries = {}
        for item in all.split('*'):
            item = item.strip()
            data = item.split('#')
            country = data[0].replace('\t', ' ').strip().lower()
            capital = data[1].lower()

            value = {country : capital}
            countries.update(value)

        return countries

    def __init__(self, member:discord.Member):
        self.name = str(member)
        self.id = member.id
        self.mention = member.mention
        self.lifes = 3
        self.points = 0

    def __repr__(self):
        return self.name
    
    async def increase_point(self, ctx):
        self.points += 1
        await ctx.send(f"{self.mention} Correct Answer!!✅")

    async def already_used(self, ctx, place):
        await self.cut_life(ctx, reason=f'used {place}')
    
    async def cut_life(self, ctx, reason:str):
        self.lifes -= 1
        if reason == 'incorrect':
            if self.lifes == 0:
                await ctx.send(f"{self.mention} Incorrect response")
                await self.eliminate(ctx)
            else:
                await ctx.send(f"{self.mention} Incorrect response, life decreased by 1\nTotal lifes left **{self.lifes}**")
        elif reason == 'timeout':
            if self.lifes == 0:
                await ctx.send(f"{self.mention}You failed to respond within time")
                await self.eliminate(ctx)
            else:
                await ctx.send(f"{self.mention} You failed to respond within time, life decreased by 1\nTotal lifes ")
        elif reason.startswith('used'):
            if self.lifes == 0:
                await ctx.send(f"{self.mention} ***{reason[5:]}*** is already used by someone")
                await self.eliminate(ctx)
            else:
                await ctx.send(f"{self.mention} ***{reason[5:]}*** is already used by someone, you can't use it again, life decreased by 1")            

    async def eliminate(self, ctx):
        Atlas.Players.pop(Atlas.Players.index(self))
        await ctx.send(f"{self.mention} You're eliminated from the game.")
        if len(Atlas.Players) == 1:
            await Atlas.won(ctx, Atlas.Players[0])
    
    def used(place):
        Atlas.Used_places.append(place)

    def jumble():
        indexes = []
        jumbled = []
        spacer = 0
        for i in range(len(Atlas.Players)):
            jumbled.append(None)
            indexes.append(spacer)
            spacer += 1
        for player in Atlas.Players:
            index = random.choice(indexes)
            jumbled[index] = player
            indexes.pop(indexes.index(index))

        Atlas.Players = jumbled

    def valid_place(place:str):
        places = Atlas.fetch_countries()
        if place.lower() in places.keys():
            print('Haan sahi place hai')
            return True
        elif place .lower() in places.values():
            print('Haan sahi place hai')
            return True
        else:
            possible_correction = SpellChecker().correction(place)
            if possible_correction.lower() in places.keys():
                print('Haan sahi place hai')
                return True
            elif possible_correction.lower() in places.values():
                print('Haan sahi place hai')
                return True
            else:
                print('Galat place hai bsdk')
                return False

    async def start(ctx):
        Atlas.current_player = Atlas.Players[0]
        await ctx.send(f"{Atlas.current_player.mention} It's your turn, start the game by giving a name of a country or capital")
        def check(m):
            return m.channel.id == ctx.channel.id and m.author.id == Atlas.current_player.id
        try:
            response = await bot.wait_for('message', check=check, timeout=10)
            return response.content
        except asyncio.TimeoutError:
            return None

    async def ask(ctx, last_letter:str):
        await ctx.send(f"{Atlas.current_player.mention} Give a name of a country or a capital by the starting letter of ***{last_letter.upper()}***")
        def check(m):
            return m.channel.id == ctx.channel.id and m.author.id == Atlas.current_player.id
        try:
            response = await bot.wait_for('message', check=check, timeout=10)
            return response.content
        except asyncio.TimeoutError:
            return None

    async def won(ctx, player):
        Atlas.End = True
        await ctx.send(f"{player.mention} You've won the game!!")

    async def correct_response(ctx):
        await Atlas.current_player.increase_point(ctx)
        if Atlas.current_player.points == 3:
            await Atlas.won(ctx, Atlas.current_player)

    async def wrong_response(ctx):
        await Atlas.current_player.cut_life(ctx, reason='incorrect')

    async def timeout(ctx):
        await Atlas.current_player.cut_life(ctx, reason='timeout')

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
            embed = discord.Embed(title=f'**Atlas**', description='react on this message with the check to participate ✅')
            embed.set_footer(icon_url='https://cdn.discordapp.com/emojis/892751786719469598.gif?size=56', text='Good luck')
            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')
        
            await asyncio.sleep(5)

            await ctx.send('Registration closed')
            cached_msg = discord.utils.get(bot.cached_messages, id=message.id)
            for reaction in cached_msg.reactions:
                if reaction.emoji == '✅':
                    users = await reaction.users().flatten()
                    for user in users:
                        if user.id != winsy_id:
                            player = Atlas(user)
                            Atlas.Players.append(player)
            print('Players before jumbled:', Atlas.Players)
            Atlas.jumble()
            print('Players after jumbled:', Atlas.Players)

            if Atlas.Players == []:
                await ctx.send('No players reacted, the game is terminated.')
                
            elif len(Atlas.Players) < 2:
                await ctx.send('Atleast 2 players are needed to start the game.')

            else:
                await ctx.send('Game starts now!!')

                first_reply = await Atlas.start(ctx)
                if first_reply != None:
                    if Atlas.valid_place(first_reply):
                        Atlas.used(first_reply)
                        await Atlas.correct_response(ctx)
                    else:
                        await Atlas.wrong_response(ctx)
                else:
                    await Atlas.timeout(ctx)

                Pointer = 1
                First = True
                Last_letter = None
                while True:
                    if Atlas.End == False:
                        if Pointer == len(Atlas.Players):
                            Pointer = 0
                        
                        Atlas.current_player = Atlas.Players[Pointer]
                        if First:  
                            Response = await Atlas.ask(ctx, last_letter=first_reply[-1])
                            Last_letter = first_reply[-1]
                            First = False
                        else:
                            Response = await Atlas.ask(ctx, last_letter=Last_letter)

                        print("Response: {}".format(Response))
                        if Response != None:
                            if Response in Atlas.Used_places:
                                await Atlas.current_player.already_used(ctx, Response)
                            elif Atlas.valid_place(Response):
                                Atlas.used(Response)
                                await Atlas.correct_response(ctx)
                            else:
                                await Atlas.wrong_response(ctx)
                        else:
                            await Atlas.timeout(ctx)

                        Pointer += 1
                    else:
                        break

@bot.command()
async def amogus(ctx):
    def crewlist(list):
        ctr = 1
        dialouge = ""
        for member in list:
            if ctr == 1:
                dialouge += f"{ctr}. {member.name}"

            else:
                dialouge += f"\n{ctr}. {member.name}"
            ctr += 1

        embed = discord.Embed(title='**Crewmates**', description='*There is one imposter among us...*', color=color())
        embed.add_field(name="List", value=dialouge, inline=False)
        embed.set_footer(icon_url='https://cdn.discordapp.com/emojis/892750347599233034.gif?size=128', text="Get ready for the fun")

        return embed

    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=Embeds.non_dm_embed())

    else:
        guild_id = ctx.guild.id
        if guild_id not in ignored.guilds:
            ignored.addguild(guild_id)
        if ctx.author.id in ignored.guilds[guild_id]:
            return
        else:
            embed = discord.Embed(title=f'Game', description='React on this message with the check to participate ✅')
            embed.set_footer(icon_url='https://cdn.discordapp.com/emojis/892751786719469598.gif?size=56', text='Amogus')
            message = await ctx.send(embed=embed)
            await message.add_reaction('✅')
            participants = []
            def check(reaction, user):
                if user.id != winsy_id:
                    if str(reaction.emoji) == '✅' and reaction.message == message:
                        participants.append(user)
                        return False
            try:
                reaction = await bot.wait_for('reaction_add', timeout=5, check=check)

            except asyncio.TimeoutError:
                await ctx.send('Registration closed.')
                print(participants)
                embed = crewlist(participants)
                crewlist = await ctx.send(embed=embed)
                msg = await ctx.send(content=f"The imposter is being decided..... {get_emoji(890871150941450271)}")
                imposter = random.choice(participants)
                await imposter.send(f"You are the imposter {get_emoji(892839909302358056)} Good luck killing those dumb fucks {get_emoji(892772725343535104)}")
                await msg.edit(content='Imposter has been decided, find the imposter once your turn comes over.')
                await ctx.send(f"Let's start shall we? {get_emoji(881253669083955221)}")
                await asyncio.sleep(2)
                while True:
                    ctr = 0
                    mate  = participants[ctr]
                    await ctx.send(f"{mate.mention} Whome do you sus? provide a reason for the others to think over it, a voting will start under 10 seconds of your relpy")
                    def check2(m):
                        return m.author == mate and m.channel == ctx.channel
                    
                    try:
                        message = await bot.wait_for('message', timeout=15, check=check2)
                        query = await ctx.send(f"Does everyone agree with {mate.mention}'s accuse")

                    except asyncio.TimeoutError:
                        await ctx.send(f"{mate.mention} you didn't reply within time....hmmm isn't that sus mates? {get_emoji(892842878848602114)}")
                        query = await ctx.send(f"Do you guys want to vote {mate.mention}?")
                        await query.add_reaction('✅')
                        global reactions
                        reactions = 0
                        def reaction_check(reaction, user):
                            global reactions
                            if reaction.emoji == '✅' and reaction.message == query:
                                reactions += 1
                                return False

                        try:
                            reactions = await bot.wait_for('reaction_add', timeout=5, check=reaction_check)

                        except asyncio.TimeoutError:
                            await query.delete()
                            print(f"reactions = {reactions}")
                            if reactions > len(participants) // 2:
                                await ctx.send("Whoops, seems like majority chose to kick you, *Happy journey!*")
                                await ctx.send("*Kicked*")
                                mute_role = discord.utils.get(my_guild.roles, name='mute')
                                mate.add_role(mute_role)
                            
                            else:
                                await ctx.send(f"{mate.mention} Lucky bro you're safe {get_emoji(881253669083955221)}")
                    
                    await query.add_reaction('✅')
                    global reactions1
                    reactions1 = 0
                    def reactions_check(reaction, user):
                        global reactions1
                        if user.id != winsy_id:
                            if reaction.message == query:
                                reactions1 += 1
                                return False
                        
                    try:
                        pass

                    except asyncio.TimeoutError:
                        pass

                    ctr += 1

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
            file = discord.File(f"Winsy/bro_fist/e4579003-ac2f-478d-874e-da4ad0f25cf0.jpg")
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

                    await ctx.message.reply(f"{dialouge}{emoji}")

                else:
                    dict = await fetch_roasts(member.id)
                    roasts = dict.get('roasts')
                    type = dict.get('type')
                    roast_choice = random.choice(roasts)
                    if type == 'Normal':
                        await ctx.send(f"{member.mention} {roast_choice}")

                    else:
                        await ctx.send(roast_choice)

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

# @bot.event
# async def on_command_error(ctx, error):
#     channel = bot.get_channel(error_channel_id)
#     embed = discord.Embed(title='Error raised in '+str(ctx.command), description=error, color=color())
#     await channel.send(embed=embed)

all_cogs = os.listdir('./Winsy/cogs')
for file in all_cogs:
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

with open('./TOKENS/token.txt', 'r') as file:
    TOKEN = file.read()

bot.run(TOKEN)