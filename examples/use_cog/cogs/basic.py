import asyncio
from mipa.ext import commands
from mipa.ext.commands.bot import Bot
from mipa.ext.commands.context import Context

class BasicCog(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
    
    @commands.mention_command(text='hello')
    async def hello(self, ctx: Context):
        await ctx.message.api.action.reply(f'hello! {ctx.message.author.username}')


    @commands.mention_command(regex=r'(\d+) second timer')
    async def timer(self, ctx: Context, time: str):
        await ctx.message.api.action.reply(f'That\'s  {time} seconds. Okay, start')
        await asyncio.sleep(int(time))
        await ctx.message.api.action.reply(f'{time} seconds have passed!')


async def setup(bot: Bot):
    await bot.add_cog(BasicCog(bot))
