import discord
from discord.ext import commands
from pymongo import MongoClient
from discord import utils
from EZPaginator import Paginator
import os

coll = MongoClient('mongodb://localhost:27017/').All_Servers.user


class Core(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.coll = coll

    @commands.group(name='서버')
    async def s(self, ctx):
        if ctx.invoked_subcommand == None:
            command = ['as서버 등록', 'as서버 삭제', 'as서버 업', 'as서버 목록']
            des = ['현재 명령어를 사용한 서버를 등록합니다.', '현재 명령어를 사용한 서버를 삭제합니다.', '현재 명령어를 사용한 서버를 업 시킵니다.', '등록된 모든 서버의 목록을 불러옵니다.']
            embed = discord.Embed(title='All Servers 도움말', description='접두사는 `as`, `ㅁㄴ`입니다.', color=0x00FFFF)

            for i in command:
                embed.add_field(name=f'> `{i}`', value=str(des[0]), inline=False)
                del des[0]
            await ctx.reply(embed=embed)

    @s.command(name='등록', aliases=['emdfhr', 'add'])
    async def add_server(self, ctx):

        if self.coll.find_one({"_id": str(ctx.guild.name)}):
            await ctx.reply('이 서버가 이미 등록되어있습니다!\n`as업` 으로 서버를 상단에 노출 시킬 수 있습니다.')

        else:
            await ctx.reply(f'`{ctx.guild.name}` 서버의 **영구** 초대 링크를 지금 입력해주세요.')

            def check(m):
                return m.channel == ctx.channel and m.author == ctx.author

            msg = await self.bot.wait_for('message', check=check)
            m = msg.content

            await ctx.reply(f'`{ctx.guild.name}` 서버의 설명을 지금 입력해주세요.')

            msgm = await self.bot.wait_for('message', check=check)
            mm = msgm.content

            if 'https://discord.gg/' in m:

                self.coll.insert_one({
                    "_id": str(ctx.guild.name),
                    "invite": str(m)
                })

                guild = self.bot.get_guild(829561316636491796)
                category = discord.utils.get(guild.categories, name='<< SERVER >>')
                channel = await guild.create_text_channel(f'{str(ctx.guild.name)}', category=category)

                if os.path.isfile(f'Servers/{str(ctx.guild.name)}.txt'):

                    with open(f'Servers/{str(ctx.guild.name)}.txt', 'a', encoding="UTF-8") as f:
                        f.write(mm)

                else:

                    with open(f'Servers/{str(ctx.guild.name)}.txt', 'a', encoding="UTF-8") as f:
                        f.write(mm)

                await ctx.reply('서버 등록이 완료되었습니다!')

            else:
                await ctx.reply('초대 링크가 알맞지 않은 것 같습니다.\n초대링크에 `https://discord.gg/`가 들어가야 합니다.')

    @s.command(name='삭제', aliases=['tkrwp', 'delete'])
    async def del_server(self, ctx):
        if self.coll.find_one({"_id": str(ctx.guild.name)}):
            if ctx.author.guild_permissions.administrator:
                await ctx.reply('정말로 삭제하시겠습니까?\n삭제하시려면 `서버 삭제 동의`를 입력해주세요.')

                def check(m):
                    return m.channel == ctx.channel and m.author == ctx.author

                msg = await self.bot.wait_for('message', check=check)
                m = msg.content

                if m == '서버 삭제 동의':
                    self.coll.delete_one({"_id": str(ctx.guild.name)})
                    guild = self.bot.get_guild(829561316636491796)
                    channel = discord.utils.get(guild.channels, name=str(ctx.guild.name))
                    cid = channel.id
                    ci = self.bot.get_channel(int(cid))
                    await ci.delete() # All Servers 에 등록되어 있는 서버 이름에 대한 채널을 삭제

                    os.remove(f"Servers/{str(ctx.guild.name)}.txt")
                    await ctx.reply('서버 삭제가 완료되었습니다.')

                else:
                    await ctx.reply('서버 삭제가 중지되었습니다.')
            else:
                await ctx.reply(f'해당 서버(`{ctx.guild.name}`)의 관리자가 아니기 때문에 서버 삭제 명령어를 이용할 수 없습니다.')
        else:
            await ctx.reply('해당 서버는 등록되어있지 않습니다.')

    @s.command(name='업', aliases=['up', 'djq'])
    async def Up(self, ctx):
        c = self.bot.get_channel(829608452384096288) # 서버들 채널
        guild = self.bot.get_guild(829561316636491796) # All Servers 서버

        channel = discord.utils.get(guild.channels, name=f'{str(ctx.guild.name)}')
        channel_id = channel.id

        channel = self.bot.get_channel(int(channel_id))

        await channel.edit(positioin=0)

        with open(f"Servers/{str(ctx.guild.name)}", "r", encoding="UTF-8") as f:
            text = f.readlines()

        sl = ''.join(text[0:])

        embed = discord.Embed(title=f'{str(ctx.guild.name)}', description=str(sl), color=0x00FFFF)
        await c.send(embed=embed)

        await ctx.reply('서버를 최상단에 업로드 했습니다!')

    @s.command(name='목록', alises=['ahrfhr', 'list'])
    async def server_list(self, ctx):
        cc = await ctx.send('<a:Load:829625589852930108> 데이터를 불러오는 중입니다.')
        l = []
        guild = self.bot.get_guild(829561316636491796)  # All Servers 서버
        category = discord.utils.get(guild.categories, name='<< SERVER >>')

        file_list = os.listdir('./Servers/')

        for n in file_list:

            with open(f"Servers/{n}", "r", encoding="UTF-8") as f:
                text = f.readlines()

            n = n.replace(".txt", "")
            sl = ''.join(text[0:])
            embed = discord.Embed(title=f'{n}', description=f'{sl}', color=0x00FFFF)
            l.append(embed)
        await cc.delete()
        msg = await ctx.reply(embed=l[0])
        await Paginator(
            bot=self.bot, message=msg, embeds=l, only=ctx.author
        ).start()



def setup(bot):
    bot.add_cog(Core(bot))