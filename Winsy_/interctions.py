import interactions

with open("./TOKENS/token.txt", 'r') as file:
    TOKEN = file.read()

bot = interactions.Client(token='ODczNTA0ODEwMjc4NzM5OTg4.YQ5Yvw.0Y1Qd1vSOr7i2iZTimyt9SRCZNQ')

@bot.command(name="hehe", description="timepass", scope=1234567890)
async def _test(ctx):
    await ctx.send("hello")

bot.start()