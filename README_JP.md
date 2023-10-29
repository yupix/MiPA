# MiPA

<a href="https://discord.gg/CcT997U"><img src="https://img.shields.io/discord/530299114387406860?style=flat-square&color=5865f2&logo=discord&logoColor=ffffff&label=discord" alt="Discord server invite" /></a>
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMiPA?ref=badge_shield" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMiPA.svg?type=shield"/></a>

## 概要

[English](./README.md)

MiPA は[Discord.py](https://github.com/Rapptz/discord.py)
ライクな書き方ができるように作っている Misskey Bot Frameworkです。

## MiPACについて

MiPAが提供するApi Wrapperとしての機能は [MiPAC](https://github.com/yupix/mipac) と呼ばれるライブラリで管理されています。MiPAと比較して作業量が非常に多いため一緒に作業をしてくださる方を募集しています。


## サポートしているMisskey

- [Misskey Official v13](https://github.com/misskey-dev/misskey)
- [Misskey Official v12](https://github.com/misskey-dev/misskey)
- [Misskey Official v11](https://github.com/misskey-dev/misskey)

### Examples

```py
import asyncio

from aiohttp import ClientWebSocketResponse
from mipac import Note
from mipac.models import ChatMessage

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

    async def on_chat(self, message: ChatMessage):
        print(message.user.username, message.text)
        if message.text == 'hello':
            await self.client.chat.action.send(
                f'hello! {message.user.username}',
                user_id=message.user.id
            )

if __name__ == '__main__':
    bot = MyBot()
    asyncio.run(bot.start('wss://example.com/streaming', 'your token here'))
```

より多くの例は [examples フォルダ](examples) をご覧ください。もしexamplesであなたのしたいことが分からなかった場合は遠慮なくIssueを作成してください。

## LICENSE

このプロジェクトは [MIT LICENSE](./LICENSE) で提供されます。

MiPAでは多くの部分においてDiscord.pyを参考にさせていただきました。そのため、Discord.pyのソースコードを利用させていただいている個所ではファイルの初めにDiscord.py側のライセンスを明記しています。詳しくはコードを確認してください。


[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMiPA.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMiPA?ref=badge_large)

## Special Thanks

- [Discord.py](https://github.com/Rapptz/discord.py)
    - Cogの仕組みやtask,stateの管理等多くの部分で参考にさせていただきました。

<p align="center">
    <a href="https://mipa.akarinext.org">Documentation</a>
    *
    <a href="https://discord.gg/CcT997U">Discord Server</a>
</p>
