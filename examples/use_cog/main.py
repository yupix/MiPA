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
        print(f'{note.user.username}: {note.text}')
    
    async def on_mention(self, notice: NotificationNote):
        # When overriding this event, you must call progress_command
        # with the mentioned note for mention_command to work.
        await self.progress_command(notice.note)


if __name__ == '__main__':
    bot = MyBot()
    asyncio.run(bot.start('instance url', 'your token'))