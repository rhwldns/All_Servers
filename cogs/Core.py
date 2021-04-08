import discord
from discord.ext import commands
from pymongo import MongoClient

coll = MongoClient('mongodb://localhost:27017/').All_Servers.user


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coll = coll

    @commands.group(name='서버')
    async def s(self, ctx):
        if ctx.invoked_subcommand == None:
            embed = discord.Embed(title='All Server - 서버 도움말', description='`as서버 등록 <서버 이름>` - 서버를 등록합니다. \n - 등록하려는 서버에서 이 명령어를 입력해주세요. \n\n`as서버 삭제`', color=0x00FFFF)
            await ctx.reply(embed=embed)

    @s.command(name='등록')
    async def add_server(self, ctx):

        if self.coll.find_one({"name": str(ctx.guild.name)}):
            await ctx.reply('이 서버가 이미 등록되어있습니다!\n`as업` 으로 서버를 상단에 노출 시킬 수 있습니다.')

        else:
            await ctx.reply(f'`{ctx.guild.name}` 서버의 **영구** 초대 링크를 지금 입력해주세요.')

            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author

            msg = await self.bot.wait_for('message', check=check)
            m = msg.content

            if 'https://discord.gg/' in m:

                self.coll.insert_one({
                    "_id": str(ctx.author.id),
                    "name": str(ctx.guild.name),
                    "invite": str(m)
                })
                await ctx.reply('서버 등록이 완료되었습니다!')

            else:
                await ctx.reply('초대 링크가 알맞지 않은 것 같습니다.\n초대링크에 `https://discord.gg/`가 들어가야 합니다.')

    @s.command(name='삭제')
    async def del_server(self, ctx):
        if self.coll.find_one({"name": str(ctx.guild.name)}):
            if ctx.author.guild_permissions.administrator:
                await ctx.reply('정말로 삭제하시겠습니까?\n삭제하시려면 `서버 삭제 동의`를 입력해주세요.')

                def check(m):
                    return m.channel == ctx.channel and m.author == ctx.author

                msg = await self.bot.wait_for('message', check=check)
                m = msg.content

                if m == '네':
                    self.coll.delete_one({"name": str(ctx.guild.name)})
                    await ctx.reply('서버 삭제가 완료되었습니다.')

                else:
                    await ctx.reply('서버 삭제가 중지되었습니다.')
            else:
                await ctx.reply(f'해당 서버(`{ctx.guild.name}`)의 관리자가 아니기 때문에 서버 삭제 명령어를 이용할 수 없습니다.')
        else:
            await ctx.reply('해당 서버는 등록되어있지 않습니다.')


def setup(bot):
    bot.add_cog(Core(bot))