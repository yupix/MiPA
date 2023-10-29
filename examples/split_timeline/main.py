import asyncio

from aiohttp import ClientWebSocketResponse
from mipac import Note

from mipa.ext.commands.bot import Bot
from mipa.ext.timelines.core import AbstractTimeline

class GlobalTimeline(AbstractTimeline):
    async def on_note(self, note: Note):  # This event is only received in the global timeline notes
        print(f'{note.author.username}: {note.content}')

class MyBot(Bot):
    def __init__(self):
        super().__init__()

    async def _connect_channel(self):
      await self.router.connect_channel({'global': GlobalTimeline(), 'main': None, 'home': None})

    async def on_ready(self, ws: ClientWebSocketResponse):
        await self._connect_channel()
        print('Logged in ', self.user.username)

    async def on_reconnect(self, ws: ClientWebSocketResponse):
        await self._connect_channel()

    async def on_note(self, note: Note):  # This event receives all channel notes
        print(f'{note.author.username}: {note.content}')


if __name__ == '__main__':
    bot = MyBot()
    asyncio.run(bot.start('instance url', 'your token'))