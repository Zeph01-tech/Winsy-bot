import sqlite3
import discord
import random
from discord.ext import commands

conn = sqlite3.connect('Winsy.db')

my_id = 762372102204030986
winsy_id = 873504810278739988

my_server_id = 762380604058632222

def color():
    colors = [0xFF355E,0xFD5B78,0xFF6037,0xFF9966,0xFF9933,0xFFCC33,0xFFFF66,0xFFFF66,0xCCFF00,0x66FF66,0xAAF0D1,0x50BFE6,0xFF6EFF,0xEE34D2,0xFF00CC,0xFF00CC,0xFF3855,0xFD3A4A,0xFB4D46,0xFA5B3D,0xFFAA1D,0xFFF700,0x299617,0xA7F432,0x2243B6,0x5DADEC,0x5946B2,0x9C51B6,0xA83731,0xAF6E4D,0xBFAFB2,0xFF5470,0xFFDB00,0xFF7A00,0xFDFF00,0x87FF2A,0x0048BA,0xFF007C,0xE936A7]    
    return random.choice(colors)

class Cog_atlas(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("All Cogs are loaded")
    
    @commands.command()
    async def test_cog(self, ctx):
        await ctx.send("Working")

    @commands.command()
    async def cog1(self, ctx):
        reacted_users = []
        embed = discord.Embed(title="**Atlas Game**", description="React on this message with the tick to register.", color=color())
        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
        def check(reaction, user):
            if reaction.message.id == message.id:
                if user.id != winsy_id:
                    temp_dict = {'user id' : user.id, 'name' : user.name}
                    reacted_users.append(temp_dict)
            return False
        try:
            reaction = await self.client.wait_for('reaction_add', timeout=5, check=check)

        except:
            await ctx.send('Regristration ended')
            print(reacted_users)

def setup(client):
    client.add_cog(Cog_atlas(client))