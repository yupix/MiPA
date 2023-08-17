import asyncio

from aiohttp import ClientWebSocketResponse
from mipac.models.notification import NotificationNote
from mipa.ext import commands
from mipac.models.note import Note

COGS = [
    'cogs.basic'
]

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__()

    async def _connect_channel(self):
        await self.router.connect_channel(['main', 'global'])

    async def on_ready(self, ws: ClientWebSocketResponse):
        print(f'connected: {self.user.username}')
        await self._connect_channel()
        for cog in COGS:
            await self.load_extension(cog)

    async def on_reconnect(self, ws: ClientWebSocketResponse):
        print('Disconnected from server. Will try to reconnect.')
        await self._connect_channel()
    
    async def on_note(self, note: Note):
        print(f'{note.author.username}: {note.content}')
    
    async def on_mention(self, notice: NotificationNote):

        # When using this event, if you use MENTION_COMMAND, you must call this method for it to work.
        await self.progress_command(notice)


if __name__ == '__main__':
    bot = MyBot()
    asyncio.run(bot.start('instance url', 'your token'))