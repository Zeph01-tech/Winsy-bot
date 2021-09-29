import sqlite3
import discord
import random
import os
import bitly_api
import requests
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio

bot = commands.Bot(command_prefix=commands.when_mentioned_or("Winsy ", "winsy "))
bot.remove_command('help')

conn = sqlite3.connect("Winsy.db")

my_id = 762372102204030986
winsy_id = 873504810278739988
flextai_id = 761943416002576385
bhavani_id = 822111796982710294
prosaber_id = 703611534395572315
mivir_id = 652469666421276681
kekda_id = 573732812289736724
romi_id = 731043362907619332
hemant_id = 852642856866414622

my_server_id = 762380604058632222
prosaber_server_id = 770130068172832798

error_channel_id = 887385480679788574

bro_fist_replies = ["**Yesss boss!**", "**BRO FIST!!!**", "**Zhong Zhong**"]
good_night_replies = ["**Oyasumi!**", "**Night!**", "**Have a great night**", "**Sweet dreams**"]

good_night_gifs = ["https://c.tenor.com/3fAZZncIHDQAAAAC/smile-anime.gif", "https://c.tenor.com/ouo5podnrgUAAAAS/cuddle-love.gif", "https://c.tenor.com/01cElrH1Ed8AAAAS/anime-shiro.gif", "https://c.tenor.com/Bn_E6t9-m_wAAAAC/sleeping-kiss.gif", "https://c.tenor.com/3eouI6QChiEAAAAC/anime-cuteness.gif", "https://c.tenor.com/tVBrvOB5ttkAAAAC/11-sad.gif"]
laugh_command_gifs = ["https://cdn.discordapp.com/attachments/873552851157254144/874619767749758986/hehe.gif", "https://c.tenor.com/fqRNsILmXHQAAAAC/anime-girl.gif", "https://cdn.discordapp.com/attachments/873552851157254144/874620123930038282/natsu-lol.gif", "https://c.tenor.com/qEfogXAprQoAAAAC/nichijou-laughing.gif", "https://c.tenor.com/fbWCY-1exTsAAAAS/bokura-wa-minna-kawaisou-gifs-to-reaction.gif"]

def color():
    colors = [0xFF355E,0xFD5B78,0xFF6037,0xFF9966,0xFF9933,0xFFCC33,0xFFFF66,0xFFFF66,0xCCFF00,0x66FF66,0xAAF0D1,0x50BFE6,0xFF6EFF,0xEE34D2,0xFF00CC,0xFF00CC,0xFF3855,0xFD3A4A,0xFB4D46,0xFA5B3D,0xFFAA1D,0xFFF700,0x299617,0xA7F432,0x2243B6,0x5DADEC,0x5946B2,0x9C51B6,0xA83731,0xAF6E4D,0xBFAFB2,0xFF5470,0xFFDB00,0xFF7A00,0xFDFF00,0x87FF2A,0x0048BA,0xFF007C,0xE936A7]    
    return random.choice(colors)

async def fetch_roasts(member_id, author_id):
    if member_id == my_id:
        type = 'Yash victim'
    
    elif member_id == winsy_id:
        if author_id == my_id:
            type = 'Winsy victim, Yash roaster'

        else:
            type = 'Winsy victim'

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
        embed = discord.Embed(description=f'**Download link of the {choice} you searched for: {link}**', color=color())

    return embed

def non_dm_embed():
    embed = discord.Embed(title='Note.', description="Commands can't be used through dms.", color=color())
    return embed

async def shorten_url(url):
    token = 'c2fe6b80d67ad910a7cee6a6698d36a50575d307'

    conn = bitly_api.Connection(access_token=token)
    reponse = conn.shorten(url)
    new_url = reponse['url']
    return new_url

@bot.event
async def on_ready():
    print("I'm logged in yay!")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="winsy help"))

@bot.command()
async def help(ctx, *, category = None):
    if category is None:
        embed = discord.Embed(title="***Help panel***", description="List of categories of all commands", color=color())
        embed.add_field(name="*mention commands :nerd:*", value="`winsy help mention cmds`", inline=False)
        embed.add_field(name="*image commands*", value="`winsy help image cmds`", inline=False)
        embed.add_field(name="*interactive commands*", value="`winsy help interactive cmds`", inline=False)
        embed.add_field(name="*search commands*", value="`winsy help search cmds`", inline=False)
        embed.set_footer(text="type a command along with category name")
        await ctx.send(embed=embed)
    
    elif category == "mention cmds":
        embed = discord.Embed(title="***Mention commands***", description="All mention commands.", color=color())
        embed.add_field(name="`gae <user mention>`", value="*Gives the gay percentage of the mentioned user*", inline=False)
        embed.add_field(name="`roast <user mention>`", value="*Sends a random roast to the mentioned user*", inline=False)
        embed.add_field(name="`spam <number of times> <user mention> <message(if any)>`", value="*Spams the message along with the mentioned user*", inline=False)
        embed.add_field(name="`poop at <user mention>`", value="*Poops in the dm of the mentioned user*", inline=True)
        await ctx.send(embed=embed)
        await ctx.message.delete()
    
    elif category == "image cmds":
        embed = discord.Embed(title="***Image commands***", description="All the image commands.", color=color())
        embed.add_field(name="`face <user mention>`", value="*Sends the face of the mentioned user if it is present in database(currently unavailable)*", inline=False)
        embed.add_field(name="`allfaces`", value="*Sends all the registered faces of user(currently unavailable)*", inline=False)
        await ctx.send(embed=embed)
        await ctx.message.delete()

    elif category == "search cmds":
        embed = discord.Embed(title="**Search commands**", description="All the search commands", color=color())
        embed.add_field(name="`reel <reel link>`", value="Sends the direct reel video link for the user to download", inline=False)
        embed.add_field(name='`yt <vid link>`', value="Sends the direct video link for the user to download", inline=False)
        await ctx.send(embed=embed)
        await ctx.message.delete()

    elif category == "interactive cmds":
        embed = discord.Embed(title="**Interactive commands**", description="All the commands to interact with the bot.", color=color())
        embed.add_field(name="`goodnight`", value="Possible aliases: `gn`, `oyasumi` *Winsy wishes goodnight*", inline=False)
        embed.add_field(name="`laugh at <user mention>`", value="*Winsy laughs at the mentioned user*", inline=False)
        embed.add_field(name="`brofist`", value="*Winsy wishes **brofist***", inline=False)
        await ctx.send(embed=embed)
        await ctx.message.delete()

@commands.cooldown(1, 60, commands.BucketType.member)
@bot.command()
async def poop(ctx, at=None, member:discord.Member=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=non_dm_embed())

    else:
        if at == 'at' or at == 'At' or at == 'aT' or at == 'AT':
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

@bot.command()
async def ping(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=non_dm_embed())
        
    else:
        await ctx.send(f"Pong! {round(bot.latency*1000, 1)}ms")

@bot.command()
async def insta(ctx, url:str=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(non_dm_embed())

    else:
        if url == None:
            await ctx.send('Provide a URL.')

        else:
            message = await ctx.send('Checking the URL')
            if url.startswith('https://www.instagram.com/') == False:
                await message.edit(content='The URL which was specified was either not a reel or an unexpected URL.')

            else:
                await message.edit(content='Processing your request, this may take some time.....')
                try:
                    api = 'https://dl.instavideosave.com/allinone'

                    headers = {'url' : url}

                    response = requests.get(url=api, headers=headers).json()

                except:
                    await message.edit(content="The request was not fullfilled for some reason.")
                    return

                try:
                    post_url = response['video']
                    embed = await embed_maker(link=await shorten_url(post_url[-1])+'video')
                    await message.delete()
                    await ctx.send(embed=embed)
                except:
                    try:
                        post_url = response['image']
                        embed = await embed_maker(link=await shorten_url(post_url[-1])+'video')
                        await message.delete()
                        await ctx.send(embed=embed)
                    except:
                        await message.edit(content="The post seems to be from a private account.")

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
        await ctx.send(embed=non_dm_embed())
        
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
                        api = "https://yt1s.com/api/ajaxConvert/convert"
                        data = {'vid' : vid_id, 'k' : audios_dict['k']}
                        response = requests.post(api, data=data).json()
                        d_link = await shorten_url(response['dlink'])
                        embed = await embed_maker(link=d_link + 'audio')
                        await ctx.send(embed=embed)
            except:
                await message.edit('Seems the like servers are down')

@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command()
async def spam(ctx, times=None, member:discord.Member=None, *, message=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=non_dm_embed())
        
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
@has_permissions(manage_roles=True)
async def purge(ctx, amount:int=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=non_dm_embed())
        
    else:
        if amount == None:
            await ctx.send("Mention the amount of messages you want to purge")
        else:
            await ctx.channel.purge(limit=amount+1)

@bot.command()
async def laugh(ctx, at, member:discord.Member=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=non_dm_embed())
        
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
        await ctx.send(embed=non_dm_embed())
        
    else:
        choice = random.choice(good_night_replies)
        choice_gif = random.choice(good_night_gifs)
        embed = discord.Embed(description=f"**{choice}** {ctx.author.mention}", colour=color())
        embed.set_image(url=choice_gif)
        await ctx.send(embed=embed) 

@bot.command()
async def brofist(ctx):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=non_dm_embed())
        
    else:
        file = discord.File(f"Winsy/bro_fist/e4579003-ac2f-478d-874e-da4ad0f25cf0.jpg")
        embed = discord.Embed(description=f"**{random.choice(bro_fist_replies)}** {ctx.author.mention}", colour=color())
        embed.set_image(url=f"attachment://e4579003-ac2f-478d-874e-da4ad0f25cf0.jpg")
        await ctx.send(file=file, embed=embed)

@bot.command(aliases=["gay"])
async def gae(ctx, member:discord.Member=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=non_dm_embed())
        
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
        await ctx.send(embed=non_dm_embed())
        
    else:
        if member == None:
            await ctx.send("You need to mention a user to roast")
        else:
            dict = await fetch_roasts(member.id, ctx.author.id)
            roasts = dict.get('roasts')
            type = dict.get('type')
            choice = random.choice(roasts)
            if type == 'Normal':
                await ctx.send(f"{member.mention} {choice}")

            else:
                await ctx.send(choice)

@bot.command()
async def why(ctx, insult=None, member:discord.Member=None):
    if isinstance(ctx.channel, discord.channel.DMChannel):
        await ctx.send(embed=non_dm_embed())
        
    else:
        if insult == 'insult':
            if member is not None:
                await ctx.send(f"{member.mention} I'm not insulting you. I'm describing you.")
            else:
                await ctx.send(f"{ctx.author.mention} I'm not insulting you. I'm describing you.")
        
        else:
            return

@bot.event
async def on_command_error(ctx, error):
    channel = bot.get_channel(error_channel_id)
    embed = discord.Embed(title='Error raised in '+str(ctx.command), description=error, color=color())
    await channel.send(embed=embed)

all_cogs = os.listdir('./Winsy/cogs')
for file in all_cogs:
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run('ODczNTA0ODEwMjc4NzM5OTg4.YQ5Yvw.0Y1Qd1vSOr7i2iZTimyt9SRCZNQ')