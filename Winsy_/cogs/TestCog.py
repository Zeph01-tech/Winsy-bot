from discord.ext import commands
import discord
import sqlite3


conn = sqlite3.connect("./Winsy_/Winsy_main.db")

my_id = 762372102204030986
my_server_id = 762380604058632222


class TestCog(commands.Cog):
    def __init__(self, client: discord.Client):
        self.client = client
        self.my_guild = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == my_id:
            args = message.content.split()
            if args[1] == 'mems':

                if self.my_guild == None:
                    self.my_guild = await self.client.fetch_guild(my_server_id)

                cursor = conn.cursor()
                data = cursor.execute("""SELECT * FROM My_Guilds WHERE no = ?""", [args[-1]]).fetchone()
                cursor.close()

                guild_id = data[1]
                guild = await self.client.fetch_guild(guild_id)
                async for member in guild.fetch_members():
                    embed = discord.Embed(
                        title=member,
                        description=f'aka {member.display_name}'
                    ).set_thumbnail(url=member.avatar_url)

                    await message.channel.send(embed=embed)
                    

    @commands.Cog.listener()
    async def on_ready(self):
        print("New Cog loaded")

def setup(client):
    client.add_cog(TestCog(client))
