import sqlite3
import random
from discord.ext import commands

conn = sqlite3.connect('Winsy.db')

my_id = 762372102204030986
winsy_id = 873504810278739988

my_server_id = 762380604058632222

def color():
    colors = [0xFF355E,0xFD5B78,0xFF6037,0xFF9966,0xFF9933,0xFFCC33,0xFFFF66,0xFFFF66,0xCCFF00,0x66FF66,0xAAF0D1,0x50BFE6,0xFF6EFF,0xEE34D2,0xFF00CC,0xFF00CC,0xFF3855,0xFD3A4A,0xFB4D46,0xFA5B3D,0xFFAA1D,0xFFF700,0x299617,0xA7F432,0x2243B6,0x5DADEC,0x5946B2,0x9C51B6,0xA83731,0xAF6E4D,0xBFAFB2,0xFF5470,0xFFDB00,0xFF7A00,0xFDFF00,0x87FF2A,0x0048BA,0xFF007C,0xE936A7]    
    return random.choice(colors)

class Mizu_bullier(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        me = message.guild.get_member(my_id)
        if message.author.display_name == 'Mizu' and message.embeds != []:
            if message.embeds[0].title.startswith(f"Deleted messages by {str(me)[0:-5]}") or message.embeds[0].title.startswith(f"Deleted messages by {me.display_name}"):
                await message.delete()

    @commands.Cog.listener()
    async def on_ready(self):
        print("All Cogs are loaded")

def setup(client):
    client.add_cog(Mizu_bullier(client))