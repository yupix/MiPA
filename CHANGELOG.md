# Change Log

## v0.5.1

[compare changes](https://github.com/yupix/MiPA/compare/0.5.0...0.5.1)

### 🩹 Fixes

- use_cogのサンプルでprogress_commandに通知を渡していたのをノートを渡すように ([b2dde53](https://github.com/yupix/MiPA/commit/b2dde53))

### 🏡 Chore

- 通知で処理するメインチャンネルのイベントを明示的に無視するように ([da0102d](https://github.com/yupix/MiPA/commit/da0102d))
  - `mention` / `reply` / `renote` / `followed` / `receiveFollowRequest` は notification として届いたものから `on_mention` などを発火させるため、メインチャンネルのイベント側では何もしません

### ❤️ Contributors

- Yupix ([@yupix](http://github.com/yupix))

## v0.5.0

[compare changes](https://github.com/yupix/MiPA/compare/0.4.6...0.5.0)

### 🏡 Chore

- MiPACのバージョンを0.8.1以上0.9.0未満に ([64d0cb5](https://github.com/yupix/MiPA/commit/64d0cb5))
  - MiPACの最低バージョンが0.8.1に変更されています。MiPAC 0.8.0 には破壊的変更が含まれるため、詳細は [MiPACのリリースノート](https://github.com/yupix/MiPAC/releases/tag/0.8.0) をご覧ください。

### ❤️ Contributors

- Yupix ([@yupix](http://github.com/yupix))

## v0.4.6

[compare changes](https://github.com/yupix/MiPA/compare/0.4.5...0.4.6)

### 🚀 Enhancements

- Note.contentを使わずにNote.textを使うように ([df7d6c2](https://github.com/yupix/MiPA/commit/df7d6c2))

### 🩹 Fixes

- Note.authorを使わないように ([539ec26](https://github.com/yupix/MiPA/commit/539ec26))
- Ws heartbeat ([4159c6b](https://github.com/yupix/MiPA/commit/4159c6b))

### ❤️ Contributors

- Yupix ([@yupix](http://github.com/yupix))
- Xtaodada ([@omg-xtao](http://github.com/omg-xtao))

## v0.4.5

[compare changes](https://github.com/yupix/MiPA/compare/0.4.4...0.4.5)

### 🩹 Fixes

- Typo ([5aab376](https://github.com/yupix/MiPA/commit/5aab376))

## v0.4.4

[compare changes](https://github.com/yupix/MiPA/compare/0.4.3...0.4.4)

### 🚀 Enhancements

- On_reconnectを記載 ([266f887](https://github.com/yupix/MiPA/commit/266f887))

### 🏡 Chore

- Client.pyからon_readyイベントの定義を削除 ([a6327eb](https://github.com/yupix/MiPA/commit/a6327eb))

## v0.4.3

[compare changes](https://github.com/yupix/MiPA/compare/0.4.2...0.4.3)

### 🏡 Chore

- MiPACで非推奨になったloginメソッドを使用しないように ([d5ae338](https://github.com/yupix/MiPA/commit/d5ae338))

## v0.4.2

[compare changes](https://github.com/yupix/MiPA/compare/0.4.1...v0.4.2)

### 🏡 Chore

- MiPACのバージョンを0.7.0以上0.8.0まで許可するように
  - MiPACの最低バージョンが0.7.0に変更されています。詳細は [MiPACのリリースノート](https://github.com/yupix/MiPAC/releases/tag/0.7.0) をご覧ください。

### ❤️ Contributors

- Yupix ([@yupix](http://github.com/yupix))

## v0.4.1

[compare changes](https://github.com/yupix/MiPA/compare/0.4.0...v0.4.1)

### 🏡 Chore

- MiPACのバージョンを0.7.0までは許可するように ([4bc8aec](https://github.com/yupix/MiPA/commit/4bc8aec))

### ❤️ Contributors

- Yupix ([@yupix](http://github.com/yupix))

## v0.4.0

このバージョンから developブランチは v13以降のみをサポートします。今まで通りの全てのイベントがあるのは shared ブランチのみとなります

[compare changes](https://github.com/yupix/MiPA/compare/0.3.5...v0.4.0)

### 🚀 Enhancements

- MiPAC v0.6.0への対応 ([36494ef](https://github.com/yupix/MiPA/commit/36494ef))
- Python3.12を必須に ([2abd5ed](https://github.com/yupix/MiPA/commit/2abd5ed))

### 🩹 Fixes

- Timelinesがpackagesに含まれていない ([d0caa63](https://github.com/yupix/MiPA/commit/d0caa63))
- 直せる範囲で型エラーを修正 ([8e5a58d](https://github.com/yupix/MiPA/commit/8e5a58d))

### ❤️ Contributors

- Yupix ([@yupix](http://github.com/yupix))

## [0.3.5] 2023-11-18

### Fixed

- 0.3.4 では直しきれなかった一部の不具合を修正しました

## [0.3.4] 2023-11-01

### Fixed

- ほとんどのイベントで引数エラーが発生する

## [0.3.1] 2023-10-30

### Added

#### チャンネルに接続した際、チャンネル名と UUID の dict が帰ってくるように

例としては以下のような物が返ってきます。

```python
await self.router.connect_channel(['main', 'home'])
>>> {'main': 'ce9b318b-3f7b-4227-b843-1b694112567e', 'home': '934b460d-50c5-463e-b975-9db7bf6ba42d'}
```

この ID は `connect_channel` を実行した際にのみ `チャンネル名: UUID` という形式になっており他の場所で取得したい場合は `router.channel_ids` プロパティを使用する必要があります。この場合は `UUID: チャンネル名` というキーと値が逆の状態で取得されるため注意してください。

#### チャンネルを切断できるように

最初に紹介した チャンネル名と UUID の dict を用いて特定のチャンネルから切断できるようになりました。

```python
channel_ids = await self.router.connect_channel(['main', 'home'])
await self.router.disconnect_channel(channel_ids['main'])
```

#### チャンネルごとに専用のクラスを使用できるように

以下のように グローバルタイムラインに対して `AbstractTimeline` を継承した `GlobalTimeline` を実装することで作成が可能です。 `on_note` メソッドを抽象クラスに沿って作成する必要もあります。また、別にクラスを渡したくないけど、チャンネルには接続したいという場合は `None` を値として渡してください。

注意点として、チャンネル専用のクラスを渡したからと言って、今回の場合でいう `MyBot` クラスにある `on_note` が発火されなくなるわけではありません。この機能の追加は多くのチャンネルに接続したいが、それぞれに別々の処理を実行したい場合を想定しています。そのため、`MyBot` 側の `on_note` には今までと変わらず**全ての**チャンネルのノートが流れてきます。

```python
from aiohttp import ClientWebSocketResponse
from loguru import logger
from mipac import Note

from mipa.ext.commands.bot import Bot
from mipa.ext.timelines.core import AbstractTimeline


class GlobalTimeline(AbstractTimeline):
    async def on_note(self, note: Note):
        logger.info(f'{note.user.username}: {note.content}')

class MyBot(Bot):
    def __init__(self):
        super().__init__()

    async def _connect_channel(self):
      await self.router.connect_channel({'global': GlobalTimeline(), 'main': None, 'home': None})

    async def on_ready(self, ws: ClientWebSocketResponse):
        await self._connect_channel()
        logger.info('Logged in ', self.user.username)
```

また、この機能が追加されたからと言って、今までのコードに特別な変更は必要ありません。今まで通りの `list` 形式の引数も引き続きサポートしています。

```python
await self.router.connect_channel(['global', 'main', 'home'])
```

## [0.3.0] 2023-04-25

### Changes by Package 📦

MiPAC に破壊的変更を含む更新があるため、よく MiPAC の CHANGELOG を読むことを推奨します。

- [MiPAC](https://github.com/yupix/MiPAC/releases)

### Changed

- [@omg-xtao](https://github.com/omg-xtao) can cancel setup_logging when init client.

## [0.2.2] 2023-04-25

### Added

- v13, v12? で 絵文字が削除された際に `on_emoji_deleted` イベントを発火するように
- v13, v12? で 絵文字が更新された際に `on_emoji_updated` イベントを発火するように

### Changed

- 使用する MiPAC のバージョンを`0.4.3`に
  - 詳しい変更点は[こちらをご覧ください](https://github.com/yupix/MiPAC/releases)

### Fixed

- `Cog.listener` を使った際に型エラーが出る

## [0.2.1] 2023-03-22

### Changed

- 使用する MiPAC のバージョンを`0.4.2`に

## [0.2.0] 2023-03-20

### Added

- `setup_hook` イベントが追加されました
  - `load_extension` 等はこのイベントで行うことを推奨します
- `ExtensionNotLoaded` 例外が追加されました

### Changed

- **BREAKING CHANGES** 以下のメソッドが非同期になります
  - Cogs 内の `setup` 関数
  - `add_cog`
  - `remove_cog`
  - `load_extension`

### Fixed

- `tasks.loop` をクラス内で使用すると `self` が受け取れない

## [0.1.2] 2023-03-14

### Added

- ✨ added event `on_achievement_earned`.
- ✨ added `disconnect` method to `Client` class.

### Fixed

- incorrect URL for streaming API #16, #17

### Changed

- 使用する MiPAC のバージョンを`0.4.1`に

## [0.1.1] 2023-01-18

### Added

- ✨ feat: support all notifications #MA-11
  - `on_user_follow` when you follow a user
  - `on_user_unfollow` when you unfollow a user
  - `on_user_followed` when someone follows you
  - `on_mention` when someone mentions you
  - `on_reply` when someone replies to your note
  - `on_renote` when someone renote your note
  - `on_quote` when someone quote your note
  - `on_reaction` when someone react to your note
  - `on_poll_vote` when someone vote to your poll
  - `on_poll_end` when a poll is ended
  - `on_follow_request` when someone send you a follow request
  - `on_follow_request_accept` when someone accept your follow request

### Changed

- 使用する MiPAC のバージョンを`0.4.0`に

### Fixed

- 🐛 fix: ws reconnect
- 🐛 fix: Separate unread chat message

## [0.1.0] 2022-12-24

### Added

- ✨ feat: add .flake8 config.
- ✨ feat: To be able to capture notes.
- ✨ added event `on_note_deleted`.
- ✨ added event `on_reacted`.
- ✨ added event `on_unreacted`.
- ✨ added `router` property a `Client` class attributes.
  - 💡 Direct instantiation of the `Router` class is deprecated.
- [@omg-xtao](https://github.com/omg-xtao) ✨ feat: added `hybridTimeline` channel [#9](https://github.com/yupix/MiPA/pull/9).

### Changed

- ⬆️ feat(deps): update mipac update mipac version.
- ✨ chore: Changed `parse_` lineage functions to asynchronous.
- 💥 feat: **BREAKING CHANGE** Change event name `on_message` from `on_note`.
- 💥 feat: **BREAKING CHANGE** Required Python version is 3.11.

### Fixed

- 🐛 fix: not working command Framework.
- 🐛 fix: Chat related stuff is flowing `on_message`.
  - 💡 Please use `on_chat` in the future!
