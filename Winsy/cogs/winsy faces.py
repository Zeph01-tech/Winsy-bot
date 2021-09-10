import sqlite3
import discord
import random
from discord import utils
from discord.ext import commands

conn = sqlite3.connect('Winsy.db')

my_id = 762372102204030986
winsy_id = 873504810278739988

my_server_id = 762380604058632222

def color():
    colors = [0xFF355E,0xFD5B78,0xFF6037,0xFF9966,0xFF9933,0xFFCC33,0xFFFF66,0xFFFF66,0xCCFF00,0x66FF66,0xAAF0D1,0x50BFE6,0xFF6EFF,0xEE34D2,0xFF00CC,0xFF00CC,0xFF3855,0xFD3A4A,0xFB4D46,0xFA5B3D,0xFFAA1D,0xFFF700,0x299617,0xA7F432,0x2243B6,0x5DADEC,0x5946B2,0x9C51B6,0xA83731,0xAF6E4D,0xBFAFB2,0xFF5470,0xFFDB00,0xFF7A00,0xFDFF00,0x87FF2A,0x0048BA,0xFF007C,0xE936A7]    
    return random.choice(colors)

async def fetch_face(member_id):
    def dict_maker(length, pics):
        dict = {}
        for i in range(length):
            dict.update({i : pics[i]})

        dict.update({'length' : length})
        return dict

    repo_dict = {}
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM faces WHERE user_id = ?""", [member_id])
    response = cursor.fetchall()
    length = len(response)
    pic_list = []
    for tuple in response:
        pic_list.append(tuple[1])

    repo_dict.update(dict_maker(length, pic_list))
    return repo_dict

class Cog_atlas(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("All Cogs are loaded")

    # @commands.Cog.listener()
    # async def on_raw_reaction_add(self, payload):
    #     channel = self.client.get_channel(payload.channel_id)
    #     await channel.send("gaes")
    
    @commands.command()
    async def test_cog(self, ctx):
        await ctx.send("Working")

    # @commands.command()
    # async def face(self, ctx, member:discord.Member=None):
    #     if ctx.guild.id == my_server_id:
    #         data = await fetch_face(member.id)
            
       

def setup(client):
    client.add_cog(Cog_atlas(client))