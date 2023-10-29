"""
The MIT License (MIT)

Copyright (c) 2015-present Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

The Software is modified as follows:
    - Delete unused functions and method.
    - Removing functions beyond what is necessary to make it work.
    - Simplification of some functions.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from __future__ import annotations

import asyncio
import inspect
import logging
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    Generic,
    TypedDict,
    TypeVar,
)

from mipac.models import Note
from mipac.models.chat import ChatMessage
from mipac.models.emoji import CustomEmoji
from mipac.models.note import NoteDeleted
from mipac.models.notification import (
    NotificationAchievement,
    NotificationFollow,
    NotificationFollowRequest,
    NotificationNote,
    NotificationPollEnd,
    NotificationReaction,
)
from mipac.models.reaction import PartialReaction
from mipac.models.user import UserDetailed
from mipac.types import INote
from mipac.types.chat import IChatMessage
from mipac.types.emoji import ICustomEmoji
from mipac.types.note import (
    INoteUpdated,
    INoteUpdatedDelete,
    INoteUpdatedReaction,
)
from mipac.utils.format import str_lower, upper_to_lower

if TYPE_CHECKING:
    from mipac.types.notification import INotification
    from mipac.types.user import IUserDetailed

    from mipa.client import Client

_log = logging.getLogger(__name__)

T = TypeVar("T")


class IMessage(TypedDict, Generic[T]):
    type: str
    body: dict[str, T]


class ConnectionState:
    def __init__(
        self,
        dispatch: Callable[..., Any],
        loop: asyncio.AbstractEventLoop,
        client: Client,
    ):
        self.__client: Client = client
        self.__dispatch = dispatch
        self.api = client.core.api
        self.loop: asyncio.AbstractEventLoop = loop
        self.parsers = parsers = {}
        for attr, func in inspect.getmembers(self):
            if attr.startswith("parse"):
                parsers[attr[6:].upper()] = func

    async def parse_emoji_added(
        self, message: Dict[str, Any], channel_id: str
    ):
        self.__dispatch(
            "emoji_add", CustomEmoji(message["body"]["emoji"], client=self.api)
        )

    async def parse_emoji_deleted(
        self, message: IMessage[list[ICustomEmoji]], channel_id: str
    ):
        self.__dispatch(
            "emoji_deleted",
            [
                CustomEmoji(emoji, client=self.api)
                for emoji in message["body"]["emojis"]
            ],
        )

    async def parse_emoji_updated(
        self, message: IMessage[list[ICustomEmoji]], channel_id: str
    ):
        self.__dispatch(
            "emoji_updated",
            [
                CustomEmoji(emoji, client=self.api)
                for emoji in message["body"]["emojis"]
            ],
        )

    async def parse_channel(self, message: Dict[str, Any]) -> None:
        """parse_channel is a function to parse channel event

        チャンネルタイプのデータを解析後適切なパーサーに移動させます

        Parameters
        ----------
        message : Dict[str, Any]
            Received message
        """
        base_msg = upper_to_lower(message["body"])
        channel_type = str_lower(base_msg.get("type"))
        _log.debug(f"ChannelType: {channel_type}")
        _log.debug(f"recv event type: {channel_type}")
        if func := getattr(self, f"parse_{channel_type}", None):
            await func(
                base_msg["body"], base_msg["id"]
            )  # parse_note意外が呼ばれたらエラー出るかも
        else:
            _log.debug(f"Unknown event type: {channel_type}")

    async def parse_follow(
        self, message: IUserDetailed, channel_id: str
    ) -> None:
        """
        When you follow someone, this event will be called
        """
        user: UserDetailed = UserDetailed(
            message,
            client=self.api,
        )
        self.__dispatch("user_follow", user)

    async def parse_unfollow(self, message: IUserDetailed, channel_id: str):
        """
        When you unfollow someone, this event will be called
        """
        user: UserDetailed = UserDetailed(
            message,
            client=self.api,
        )
        self.__dispatch("user_unfollow", user)

    async def parse_signin(self, message: Dict[str, Any], channel_id: str):
        """
        ログインが発生した際のイベント
        """

    async def parse_note_updated(
        self, note_data: INoteUpdated[Any], channel_id: str
    ):
        message: Dict[str, Any] = upper_to_lower(note_data)
        if func := getattr(self, f'parse_{message["body"]["type"]}', None):
            await func(message)
        else:
            _log.debug(
                f'Unknown note_updated event type: {message["body"]["type"]}'
            )

    async def parse_deleted(
        self, note: INoteUpdated[INoteUpdatedDelete], channel_id: str
    ):
        self.__dispatch("note_deleted", NoteDeleted(note))

    async def parse_unreacted(
        self, reaction: INoteUpdated[INoteUpdatedReaction], channel_id: str
    ):
        self.__dispatch(
            "unreacted", PartialReaction(reaction, client=self.api)
        )

    async def parse_reacted(
        self, reaction: INoteUpdated[INoteUpdatedReaction], channel_id: str
    ):
        self.__dispatch("reacted", PartialReaction(reaction, client=self.api))

    async def parse_me_updated(self, user: IUserDetailed, channel_id: str):
        self.__dispatch("me_updated", UserDetailed(user, client=self.api))

    async def parse_read_all_announcements(
        self, message: Dict[str, Any], channel_id: str
    ) -> None:
        pass  # TODO: 実装

    async def parse_drive_file_created(
        self, message: Dict[str, Any], channel_id: str
    ) -> None:
        self.__dispatch("drive_file_created", message)

    async def parse_read_all_unread_mentions(
        self, message: Dict[str, Any], channel_id: str
    ) -> None:
        pass  # TODO:実装

    async def parse_read_all_unread_specified_notes(
        self, message: Dict[str, Any], channel_id: str
    ) -> None:
        pass  # TODO:実装

    async def parse_read_all_channels(
        self, message: Dict[str, Any], channel_id: str
    ) -> None:
        pass  # TODO:実装

    async def parse_read_all_notifications(
        self, message: Dict[str, Any], channel_id: str
    ) -> None:
        pass  # TODO:実装

    async def parse_url_upload_finished(
        self, message: Dict[str, Any], channel_id: str
    ) -> None:
        pass  # TODO:実装

    async def parse_unread_mention(
        self, message: Dict[str, Any], channel_id: str
    ) -> None:
        pass

    async def parse_unread_specified_note(
        self, message: Dict[str, Any], channel_id: str
    ) -> None:
        pass

    async def parse_read_all_messaging_messages(
        self, message: Dict[str, Any], channel_id: str
    ) -> None:
        pass

    async def parse_messaging_message(
        self, message: IChatMessage, channel_id: str
    ) -> None:
        """
        チャットが来た際のデータを処理する関数
        """
        self.__dispatch(
            "chat",
            ChatMessage(message, client=self.api),
        )

    async def parse_unread_messaging_message(
        self, message: IChatMessage, channel_id: str
    ) -> None:
        """
        チャットが既読になっていない場合のデータを処理する関数
        """
        self.__dispatch(
            "chat_unread_message",
            ChatMessage(message, client=self.api),
        )

    async def parse_notification(
        self, notification_data: Dict[str, Any], channel_id: str
    ) -> None:
        """
        Parse notification event

        Parameters
        ----------
        message: Dict[str, Any]
            Received message
        """
        message: INotification = upper_to_lower(notification_data)
        notification_map: dict[
            str,
            tuple[
                str,
                [
                    NotificationFollow
                    | NotificationNote
                    | NotificationReaction
                    | NotificationPollEnd
                    | NotificationFollowRequest
                ],
            ],
        ] = {
            "follow": ("user_followed", NotificationFollow),
            "mention": ("mention", NotificationNote),
            "reply": ("reply", NotificationNote),
            "renote": ("renote", NotificationNote),
            "quote": ("quote", NotificationNote),
            "reaction": ("reaction", NotificationReaction),
            "poll_vote": ("poll_vote", NotificationNote),
            "poll_ended": ("poll_end", NotificationPollEnd),
            "receive_follow_request": (
                "follow_request",
                NotificationFollowRequest,
            ),
            "follow_request_accepted": (
                "follow_request_accept",
                NotificationFollow,
            ),
            "achievement_earned": (
                "achievement_earned",
                NotificationAchievement,
            ),
        }
        dispatch_path, parse_class = notification_map.get(
            str_lower(message["type"]), (None, None)
        )
        if dispatch_path and parse_class:
            self.__dispatch(
                dispatch_path, parse_class(message, client=self.api)
            )

    async def parse_unread_notification(
        self, message: Dict[str, Any], channel_id: str
    ) -> None:
        """
        未読の通知を解析する関数

        Parameters
        ----------
        message : Dict[str, Any]
            Received message
        """
        # notification_type = str_lower(message['type'])
        # getattr(self, f'parse_{notification_type}')(message)

    async def parse_note(self, message: INote, channel_id: str) -> None:
        """
        ノートイベントを解析する関数
        """
        note = Note(message, self.api)
        await self.__client.router.capture_message(note.id)
        handler = self.__client.router.channel_handlers.get(channel_id)
        if handler:
            await handler.on_note(note)
        self.__dispatch("note", note)
