import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import bot

i = discord.Intents.all()

bot = commands.Bot(command_prefix=['as', 'ㅁㄴ'], help_command=None, intents=i)

startup_extensions = ['cogs.Core', 'cogs.Util', 'jishaku']

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('불러오기에 실패 하였습니다. 에러 파일 : {}\n에러 내용 : {}'.format(extension, exc))


@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("as도움말"))
    print('All Servers#8646 On Ready.')

@bot.command(name='ㄹ,', aliases=['f', '리로드', 'flfhem'])
async def Reload(ctx):
    for i in startup_extensions:
        bot.reload_extension(i)
    await ctx.send('리로드가 완료되었습니다.')



bot.run('TOKEN')