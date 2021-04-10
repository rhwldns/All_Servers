import discord
from discord.ext import commands
import time


class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='초대')
    async def Invite(self, ctx):
        embed = discord.Embed(title='All Servers 초대링크', description=f'[여기](https://discord.com/api/oauth2/authorize?client_id=829524992881852457&permissions=1074080849&scope=bot)를 클릭하여 All Servers 봇을 초대해주세요!', color=0x00FFFF, inline=False)
        await ctx.reply(embed=embed)


    @commands.command(name='정보', aliases=['봇 정보', '봇정보', 'information','wjdqh'])
    async def information(self, ctx):
        maind = await self.bot.fetch_user(443734180816486441)

        embed = discord.Embed(title='All Servers 정보', description=' ', color=0xffff00)
        embed.add_field(name='개발 모듈', value=f'discord.py ver {discord.__version__}\njishaku ver 1.20', inline=False)
        embed.add_field(name='개발자', value=f'메인 개발자 : {maind}', inline=False)
        embed.add_field(name='다양한 링크', value="[All Servers 서버](https://discord.gg/FVUjsa5QM7)", inline=False)
        await ctx.reply(embed=embed)

    @commands.command(name='핑', aliases=['vld', 'ping', '상태'])
    async def ping(self, ctx):
        before = time.monotonic()
        embed = discord.Embed(title=':ping_pong: 퐁!', description=' ', color=0xffff00, inline=False)
        msg = await ctx.send(embed=embed)

        ping = round((time.monotonic() - before) * 1000)

        la = round(self.bot.latency * 1000)
        embed = discord.Embed(title='퐁! :ping_pong: ', description=' ', color=0xffff00, inline=False)
        embed.add_field(name='Message', value=f'{str(ping)}ms', inline=False)
        embed.add_field(name='Gateway', value=f'{round(self.bot.latency * 1000)}ms', inline=False)
        await msg.edit(embed=embed)


def setup(bot):
    bot.add_cog(Util(bot))