import asyncio
from mipa.ext import commands
from mipa.ext.commands.bot import Bot
from mipa.ext.commands.context import Context

class BasicCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @commands.mention_command(regex=r'(\d+)秒タイマー')
    async def timer(self, ctx: Context, time: str):
        await ctx.message.api.action.reply(f'{time}秒ですね。よーいドン！')
        await asyncio.sleep(int(time))
        await ctx.message.api.action.reply(f'{time}秒経ちました！')


async def setup(bot: Bot):
    await bot.add_cog(BasicCog(bot))
