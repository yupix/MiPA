# MiPA

<a href="https://discord.gg/CcT997U"><img src="https://img.shields.io/discord/530299114387406860?style=flat-square&color=5865f2&logo=discord&logoColor=ffffff&label=discord" alt="Discord server invite" /></a>
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMiPA?ref=badge_shield" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMiPA.svg?type=shield"/></a>

## Overview

[日本語版](./README_JP.md)

MiPA is a Misskey Bot Framework created to allow for [Discord.py](https://github.com/Rapptz/discord.py)-like coding.


## About MiPAC
The API wrapper functionality provided by MiPA is managed by a library called [MiPAC](https://github.com/yupix/mipac). Since the amount of work is significantly higher than that of MiPA, we are looking for people to work with us.


## Supported Misskey Versions

- [Misskey Official v13](https://github.com/misskey-dev/misskey)
- [Misskey Official v12](https://github.com/misskey-dev/misskey)
- [Misskey Official v11](https://github.com/misskey-dev/misskey)

### Examples

```py
import asyncio

from aiohttp import ClientWebSocketResponse
from mipac.models.note import Note

from mipa.ext.commands.bot import Bot


class MyBot(Bot):
    def __init__(self):
        super().__init__()

    async def _connect_channel(self):
      await self.router.connect_channel(['main', 'home'])

    async def on_ready(self, ws: ClientWebSocketResponse):
        await self._connect_channel()
        print('Logged in ', self.user.username)

    async def on_reconnect(self, ws: ClientWebSocketResponse):
        await self._connect_channel()

    async def on_note(self, note: Note):
        print(note.author.username, note.content)


if __name__ == '__main__':
    bot = MyBot()
    asyncio.run(bot.start('wss://example.com/streaming', 'your token here'))
```

For more examples, please see the [examples folder](examples). If you don't know how to do what you want in the examples, please feel free to create an issue.




## LICENSE
This project is provided under the [MIT LICENSE](./LICENSE).

MiPA has been inspired by Discord.py in many ways. Therefore, in places where we use the source code of Discord.py, we specify the license of Discord.py at the beginning of the file. Please check the code for details.



[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMiPA.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMiPA?ref=badge_large)

## Special Thanks

- [Discord.py](https://github.com/Rapptz/discord.py)
    - We have been inspired by many aspects of Discord.py, such as the mechanism of Cogs and the management of tasks and states.

<p align="center">
    <a href="https://mipa.akarinext.org">Documentation</a>
    *
    <a href="https://discord.gg/CcT997U">Discord Server</a>
</p>
