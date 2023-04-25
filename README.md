# MiPA

<a href="https://discord.gg/CcT997U"><img src="https://img.shields.io/discord/530299114387406860?style=flat-square&color=5865f2&logo=discord&logoColor=ffffff&label=discord" alt="Discord server invite" /></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-axblack-8bd124.svg"></a>
<a href="https://app.fossa.com/projects/git%2Bgithub.com%2Fyupix%2FMiPA?ref=badge_shield" alt="FOSSA Status"><img src="https://app.fossa.com/api/projects/git%2Bgithub.com%2Fyupix%2FMiPA.svg?type=shield"/></a>

## 概要

MiPA は[Discord.py](https://github.com/Rapptz/discord.py)
ライクな書き方ができるように作っている MisskeyApi wrapper です

## 注意

### MiPACとの関係性について

MiPAはMiPACというライブラリに依存しています。これはMiPAのCore部分をまとめた物であり、基本的にはApiへのアクセス用メソッドなどを提供します。MiPAではMiPACのメソッド群をそのまま公開している為、MiPAC側で大きな変更が入るとMiPAを使用しているプロジェクトでもその影響を受ける可能性があります。そのため、[CHANGELOG.md](./CHANGELOG.md) で MiPACのバージョンが変更された際はそのリリースノートへのリンクを添付しています。予めMiPAC側での変更を確認したうえでアップデートをお願いします。

- このプロジェクトは開発中です。仕様が定まっていないため、破壊的変更が多いです。
- `master` ブランチで使用しているmipacは`GitHub`にあるmipacの`develop`ブランチの物です。

## サポートしているMisskey

- [Misskey Official v12](https://github.com/misskey-dev/misskey)
- [Ayuskey latest](https://github.com/teamblackcrystal/misskey)

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

    async def on_ready(self, ws: ClientWebSocketResponse):
        await self.router.connect_channel(['main', 'home'])
        print('Logged in ', self.user.username)

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

Want more examples? Go to the [examples folder](examples)! Want to know how to use a feature that isn't even here?
Submit a request in an Issue!


### 使用者の方へ

MiPAで作ったBotなどをGitHubなどで公開している場合は、Issueなどに送信してくだされば、MiPAで作られている物に追加します。また、良ければBotのプロフィールなどにこのBotはMiPAで作成されているとの旨を記載してくださると嬉しいです。

### MiPAで作られているもの

#### Bot

- [akari](https://github.com/teamblackcrystal/akari)
    - 作者の yupix が作成しているBotです。クリーンアーキテクチャを用いているため、部分的に分かりにくい所があるかもしれません。

### 開発者向け情報

このプロジェクトでは [black](https://github.com/psf/black)のforkである、[axblack](https://github.com/axiros/axblack)を利用しています。主な違いはダブルクォートがデフォルトではなく、シングルクォートになっている点です

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
