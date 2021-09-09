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

def fetch_face(member_id):
    # def dict_maker(length, pics):
    #     dict = {}
    #     ctr = 0
    #     for i in range(length):
    #         dict.update({ctr : pics[ctr]})
    #         ctr += 1

    #     dict.update({'length' : length})
    #     return dict

    # repo_dict = {}
    # cursor = conn.cursor()
    # cursor.execute("""SELECT * FROM faces WHERE user_id = ?""", [member_id])
    # response = cursor.fetchall()
    # length = len(response)
    # pic_list = []
    # for tuple in response:
    #     pic_list.append(tuple[1])

    # repo_dict.update(dict_maker(length, pic_list))
    # return repo_dict
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM faces WHERE user_id = ?""", [member_id])
    response = cursor.fetchall()
    pics_byte = []
    if len(response) != 0:
        for elms in response:
            pics_byte.append(elms[1])
        return pics_byte

    else:
        return False

def write_pic(bytes):
    with open('temp.jpg', 'wb') as f:
        f.write(bytes)
        f.close()

async def embed_maker(arr=None, link=None):
    if arr != None:
        index = 1
        ctr = 0
        dialouge = "**All the available qualities, send an index of the quality you want.**"
        quality_dialouge = ""
        for i in range(len(arr)):
            quality_dialouge += f'\n {index}. {arr[ctr]}'
            ctr += 1
            index += 1
        
        embed = discord.Embed(description=dialouge+quality_dialouge, color=color())

    elif link != None:
        embed = discord.Embed(description=f'**Download link of the video you searched for: {link}**', color=color())
    return embed

def edit_msg(message, file):
    asyncio.run(message.edit(file=file))

async def url_shortener(url):
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
    print(f'{ctx.author} used the command "help" in channel "{ctx.channel}"')
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
        embed.add_field(name="`face <user mention>`", value="*Sends the face of the mentioned user if it is present in database*", inline=False)
        embed.add_field(name="`allfaces`", value="*Sends all the registered faces of user*", inline=False)
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

@bot.command()
async def test(ctx):
    message = await ctx.send('React on this')
    await message.add_reaction('✅')
    def check(reaction, user):
        if user == ctx.author:
            if reaction.emoji == '✅':
                return True
            elif reaction.emoji == '❌':
                return 'X'

    while True:
        reaction = await bot.wait_for('reaction_add', check=check, timeout=None)
        if reaction == True:
            await message.edit(content="You reacted with ✅")
        elif reaction == 'X':
            await message.edit(content='Gaand it ended')
            break

@commands.cooldown(1, 60, commands.BucketType.member)
@bot.command()
async def poop(ctx, at=None, member:discord.Member=None):
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
async def reel(ctx, url:str=None):
    if url == None:
        await ctx.send('Give a URL of the reel you want to download')

    else:
        message = await ctx.send('Checking the URL')
        if url.startswith('https://www.instagram.com/') == False:
            await message.edit(content='The URL which was specified was either not a reel or an unexpected URL.')

        else:
            await message.edit(content='Processing your reel, this may take some time.....')
            try:
                api = 'https://dl.instavideosave.com/allinone'

                headers = {'url' : url}

                response = requests.get(url=api, headers=headers).json()

            except:
                await message.edit(content="The request was not fullfilled for some reason.")
                return

            try:
                vid_url = response['video']
                embed = await embed_maker(link=await url_shortener(vid_url[-1]))
                await message.delete()
                await ctx.send(embed=embed)
            except:
                try:
                    vid_url = response['image']
                    await message.edit(content='The link could not be generated.')
                except:
                    await message.edit(content='No such reel found.')

@bot.command()
async def yt(ctx, url:str=None):
    async def dict_maker(list):
        dict = {}
        ctr = 1
        for quality in list:
            new_dict_value = {ctr : quality}
            dict.update(new_dict_value)
            ctr += 1
        return dict

    if url == None:
        await ctx.send('Give a URL of the video you want to download')

    else:
        message = await ctx.send('Checking the URL')
        if url.startswith('https://youtu.be/') == False:
            await message.edit(content='The URL which was specified was either not a video or an unexpected URL.')
        
        else:
            await message.edit(content='Processing your yt video, this may take some time.....')
            try:
                api = 'https://onlinevideoconverter.pro/api/convert'
                data = {'url' : url}
                response = requests.post(api, data=data).json()
                in_url = response['url']
                available_video_qualities = []
                for dict in response['url']:
                    quality = dict['quality']
                    name = dict['name']
                    if name == 'MP4':
                        if dict['no_audio'] == False:
                            if quality not in available_video_qualities and str(quality).endswith('0'):
                                    available_video_qualities.append(quality)

                embed1 = discord.Embed(description='In which format do you want to download the file:\n **1.** *Mp4(Video)*\n**2.** *Mp3(Audio)*')
                await message.edit(embed=embed1, content="")
                def check1(m):
                    return m.author == ctx.author and m.channel == ctx.message.channel
                    
                try:
                    format_req = await bot.wait_for('message', check=check1, timeout=10)
                    choice = format_req.content
                    await format_req.delete()

                except asyncio.TimeoutError:
                    await message.delete()
                    await ctx.send('You failed to repond within time.')
                    return
                
                try:
                    int(choice)
                    if choice != '1' and choice != '2':
                        await message.delete()
                        await ctx.send('Invalid index given.')
                        return

                except:
                    await message.delete()
                    await ctx.send("Bro I'm asking for indexes here.")
                    return

                if choice == '1':
                    if "720" in response["video_quality"] and "720" not in available_video_qualities:
                        available_video_qualities.append("720")

                    embed2 = await embed_maker(arr=available_video_qualities)
                    await message.edit(embed=embed2, content="")

                    def check2(m):
                        return m.author == ctx.author and m.channel == ctx.message.channel

                    try:
                        quality_req = await bot.wait_for('message', check=check2, timeout=10)
                        msg = quality_req.content
                        await quality_req.delete()

                    except asyncio.TimeoutError:
                        await message.delete()
                        await ctx.send('You failed to respond within time.')
                        return
                    try:
                        int(msg)

                    except:
                        await message.delete()
                        await ctx.send("Bro I'm asking for indexes here.")
                        return

                    my_dict = await dict_maker(available_video_qualities)
                    in_url = response['url']
                    flag = False
                    for index in range(len(in_url)):
                        in_index = in_url[index]
                        quality = in_index['quality']
                        if quality == my_dict.get(int(msg)) and in_index['name'] == 'MP4':
                            if in_index['no_audio'] == False:
                                correct_index = index
                                flag = True
                                break
                            else:
                                continue

                    if flag == True:
                        inside_index = in_url[correct_index]
                        vid_url = inside_index['url']
                        await message.delete()
                        embed = await embed_maker(link=await url_shortener(vid_url))
                        await ctx.send(embed=embed)

                    elif my_dict.get(int(msg)) == "720":
                        exception720 = response['diffConverter']
                        embed = await embed_maker(link=await url_shortener(exception720))
                        await message.delete()
                        await ctx.send(embed=embed)

                    else:
                        await message.delete()
                        await ctx.send("Invalid index given.")

                elif choice == '2':
                    try:
                        audio_link = response['mp3Converter']
                        shortened_link = await url_shortener(audio_link)
                        embed = discord.Embed(description=f'**Download link of the audio you searched for: {shortened_link}**', color=color())
                        await message.delete()
                        await ctx.send(embed=embed)
                    except:
                        embed = discord.Embed(description="The video couldn't be converted to an audio file for some reason.")
                        await message.delete()
                        await ctx.send(embed=embed)

            except Exception as e:
                await message.edit(content='Terminal dekh bc')
                print(e)

@commands.cooldown(1, 30, commands.BucketType.user)
@bot.command()
async def spam(ctx, times=None, member:discord.Member=None, *, message=None):
    print(f'{ctx.author} used command "spam" in {ctx.channel}')
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
    if amount == None:
        await ctx.send("Mention the amount of messages you want to purge")
    else:
        await ctx.channel.purge(limit=amount+1)

@bot.command()
async def face(ctx, member:discord.Member=None):

    # if ctx.guild.id == my_server_id:
    #     member_id = member.id
    #     global data
    #     global ctr
    #     ctr = 0
    #     # while True:
    #     data = fetch_face(member.id)
    #     for x in data:
    #         print(x)
    #     with open('temp.jpg', 'wb') as f:
    #         f.write(data[0])
    #     file = discord.File('temp.jpg')
    #     embed = discord.Embed(description=f"Here's {member.mention}", colour=color())
    #     embed.set_image(url="attachment://temp.jpg")
    #     global message
    #     message = await ctx.send(embed=embed, file=file)
    #     await message.add_reaction('⬅️')
    #     await message.add_reaction('➡️')
    #     async def message_editor(fts):
    #         print("Ghus gaye andar")
    #         embed = discord.Embed(description="Gaand", color=color())
    #         embed.set_image(url="attachment://temp.jpg")
    #         await message.edit(content="lol", embed=embed,file=fts)
    #     def check(reaction, user):
    #         global ctr
    #         global data
    #         if reaction.message == message and user.id == ctx.author.id:
    #                 response_dict = fetch_face(member_id)
    #                 # ctr = get_ctr()
    #                 if str(reaction.emoji) == '➡️':
    #                     # if ctr < response_dict['length']:
    #                         ctr += 1
    #                         print(ctr)
    #                         # write_pic(data[ctr])
    #                         print(data.keys())
    #                         with open('temp.jpg', 'wb') as f:
    #                             f.write(data[1])
    #                         file = discord.File('./temp.jpg')
    #                         asyncio.run_coroutine_threadsafe(message_editor(fts=file), bot.loop)
    #                         # update_ctr(+1)

    #                 elif reaction.emoji == '⬅️':
    #                     if ctr > 0:
    #                         ctr -= 1
    #                         write_pic(response_dict.get(ctr))
    #                         file = discord.Embed('./temp.jpg')
    #                         asyncio.run_coroutine_threadsafe(message.edit(file=file), bot.loop)
                            
    #                         # update_ctr(-1)

    #         return False
    #     try:
    #         while True:
    #             reaction = await bot.wait_for('reaction_add', check=check, timeout=120)

    #     except asyncio.TimeoutError:
    #         await message.delete()
    # else:
    #     await ctx.send("This is command can't be used in this server")

    if ctx.guild.id == my_server_id:
        print(f'{ctx.author} used command "face" in channel {ctx.channel}')
        pics = fetch_face(member.id)
        if pics == False:
            await ctx.send("No data for the mentioned user in Database")
        else:
            choice = random.choice(pics)
            with open('rickroll.txt', 'r') as f:
                rick = f.read()
            if str(choice) == rick:
                with open('temp.gif', 'wb') as file:
                    file.write(choice)
                file = discord.File('temp.gif')
                embed = discord.Embed(title="You've been RICKROLLED!", colour=color())
                embed.set_image(url='attachment://temp.gif')
                embed.set_footer(text="Used from cog")
                message = await ctx.send(file=file, embed=embed)
                await message.add_reaction(":arrow_left:")
                await message.add_reaction(":arrow_right:")
            else:
                with open('temp.jpg', 'wb') as file:
                    file.write(choice)
                file = discord.File("temp.jpg")
                embed = discord.Embed(description=f"Here's {member.mention}", colour=color())
                embed.set_image(url="attachment://temp.jpg")
                embed.set_footer(text="Used from cog")
                message = await ctx.send(file=file, embed=embed)
    else:
        file = discord.File("temp.gif")
        embed = discord.Embed(title="You've been RICKROLLED!", color = color())
        embed.set_image(url="attachment://temp.gif")
        await ctx.send(file=file, embed=embed)

@bot.command()
async def allfaces(ctx, member:discord.Member=None):
    if ctx.guild.id == my_server_id:

        with open('temp.gif', 'rb') as f:
            rick_roll = f.read()

        if member is None:
            list = await fetch_face(ctx.author.id)
            for pic in list:
                if pic == rick_roll:
                    continue
        
                else:
                    with open('temp.jpg', 'wb') as f:
                        f.write(pic)

                file = discord.File('temp.jpg')
                await ctx.send(file=file, delete_after=15)

        else:
            list = await fetch_face(member.id)
            for pic in list:

                if pic == rick_roll:
                    continue

                else:
                    with open('temp.jpg', 'wb') as f:
                        f.write(pic)

                file = discord.File('temp.jpg')
                await ctx.send(file=file, delete_after=15)

    else:
        await ctx.send("This command can't be used in this server.")

@bot.command()
async def rgr(ctx):
    def reacted_user_maker(list):
        ctr = 0
        response = "These are the reacted users: "
        for i in range(len(list)):
            response += f"\n{list[ctr]}"
        return response

    list = []
    message = await ctx.send("React for registration.")
    await message.add_reaction('✅')
    def check(reaction, user):
        if reaction.message == message:
            if reaction.emoji == '✅' and user.id != winsy_id:
                list.append(user)

        return False

    try:
        reaction = await bot.wait_for('reaction_add', check=check, timeout=6)
        await ctx.send("Check true ho gaya bc")

    except asyncio.TimeoutError:
        await ctx.send("Registration closed.")
        response = reacted_user_maker(list)
        await ctx.send(response)

@bot.command()
async def laugh(ctx, at, member:discord.Member=None):
    if at == "at" or at == "At" or at == "aT" or at == "AT":
        if member is None:
            await ctx.send("Mention a user to laugh at")
        
        else:
            if member.id == winsy_id:
                await ctx.send("How foolish of you to make me laugh at myself")

            else:
                choice_gif = random.choice(laugh_command_gifs)
                embed = discord.Embed(description=member.mention, colour=color())
                embed.set_author(name=member.name, icon_url=member.avatar_url)
                embed.set_image(url=choice_gif)
                await ctx.send(embed=embed)

    else:
        return

@bot.command(aliases=["gn", "oyasumi", "Oyasumi", "Gn"])
async def goodnight(ctx):
    choice = random.choice(good_night_replies)
    choice_gif = random.choice(good_night_gifs)
    embed = discord.Embed(description=f"**{choice}** {ctx.author.mention}", colour=color())
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_image(url=choice_gif)
    await ctx.send(embed=embed) 

@bot.command()
async def brofist(ctx):
    file = discord.File(f"Winsy/bro_fist/e4579003-ac2f-478d-874e-da4ad0f25cf0.jpg")
    embed = discord.Embed(description=f"**{random.choice(bro_fist_replies)}** {ctx.author.mention}", colour=color())
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_image(url=f"attachment://e4579003-ac2f-478d-874e-da4ad0f25cf0.jpg")
    await ctx.send(file=file, embed=embed)

@bot.command(aliases=["gay"])
async def gae(ctx, member:discord.Member=None):
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
    print(f'{ctx.author} used the command "roast" in {ctx.channel}')
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
    if insult == 'insult':
        if member is not None:
            await ctx.send(f"{member.mention} I'm not insulting you. I'm describing you.")
        else:
            await ctx.send(f"{ctx.author.mention} I'm not insulting you. I'm describing you.")
    
    else:
        return

all_cogs = os.listdir('./Winsy/cogs')
for file in all_cogs:
    if file.endswith('.py'):
        bot.load_extension(f'cogs.{file[:-3]}')

bot.run('ODczNTA0ODEwMjc4NzM5OTg4.YQ5Yvw.0Y1Qd1vSOr7i2iZTimyt9SRCZNQ')