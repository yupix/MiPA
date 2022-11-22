from __future__ import annotations

import asyncio
import inspect
import logging
from typing import TYPE_CHECKING, Any, Callable, Dict

from mipac.types import INote
from mipac.util import str_lower, upper_to_lower
from mipac.models.emoji import CustomEmoji
from mipac.types.user import IUserLite
from mipac.types.chat import IChatMessage
from mipac.types.note import INoteReaction
from mipac.models import Note
from mipac.models.chat import ChatMessage
from mipac.models.user import LiteUser
from mipac.models.note import NoteReaction

if TYPE_CHECKING:
    from mipa.client import Client

_log = logging.getLogger(__name__)


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
            if attr.startswith('parse'):
                parsers[attr[6:].upper()] = func

    def parse_emoji_added(self, message: Dict[str, Any]):
        self.__dispatch(
            'emoji_add', CustomEmoji(message['body']['emoji'], client=self.api)
        )

    def parse_channel(self, message: Dict[str, Any]) -> None:
        """parse_channel is a function to parse channel event

        チャンネルタイプのデータを解析後適切なパーサーに移動させます

        Parameters
        ----------
        message : Dict[str, Any]
            Received message
        """
        base_msg = upper_to_lower(message['body'])
        channel_type = str_lower(base_msg.get('type'))
        _log.debug(f'ChannelType: {channel_type}')
        _log.debug(f'recv event type: {channel_type}')
        getattr(self, f'parse_{channel_type}')(base_msg['body'])

    def parse_renote(self, message: Dict[str, Any]):
        pass

    def parse_unfollow(self, message: Dict[str, Any]):
        """
        フォローを解除した際のイベントを解析する関数
        """

    def parse_signin(self, message: Dict[str, Any]):
        """
        ログインが発生した際のイベント
        """

    def parse_receive_follow_request(self, message: Dict[str, Any]):
        """
        フォローリクエストを受け取った際のイベントを解析する関数
        """

        # self.__dispatch('follow_request', FollowRequest(message)) TODO:修正

    def parse_me_updated(self, user: IUserLite):
        self.__dispatch('me_updated', LiteUser(user))

    def parse_read_all_announcements(self, message: Dict[str, Any]) -> None:
        pass  # TODO: 実装

    def parse_reply(self, message: INote) -> None:
        """
        リプライ
        """
        self.__dispatch('message', Note(message, client=self.__client.client))

    def parse_follow(self, message: IUserLite) -> None:
        """
        ユーザーをフォローした際のイベントを解析する関数
        """

        self.__dispatch('user_follow', LiteUser(message))

    def parse_followed(self, user: IUserLite) -> None:
        """
        フォローイベントを解析する関数
        """

        self.__dispatch('follow', LiteUser(user))

    def parse_mention(self, note: INote) -> None:
        """
        メンションイベントを解析する関数
        """

        self.__dispatch('mention', Note(note, client=self.__client.client))

    def parse_drive_file_created(self, message: Dict[str, Any]) -> None:
        self.__dispatch('drive_file_created', message)

    def parse_read_all_unread_mentions(self, message: Dict[str, Any]) -> None:
        pass  # TODO:実装

    def parse_read_all_unread_specified_notes(
        self, message: Dict[str, Any]
    ) -> None:
        pass  # TODO:実装

    def parse_read_all_channels(self, message: Dict[str, Any]) -> None:
        pass  # TODO:実装

    def parse_read_all_notifications(self, message: Dict[str, Any]) -> None:
        pass  # TODO:実装

    def parse_url_upload_finished(self, message: Dict[str, Any]) -> None:
        pass  # TODO:実装

    def parse_unread_mention(self, message: Dict[str, Any]) -> None:
        pass

    def parse_unread_specified_note(self, message: Dict[str, Any]) -> None:
        pass

    def parse_read_all_messaging_messages(
        self, message: Dict[str, Any]
    ) -> None:
        pass

    def parse_messaging_message(self, message: IChatMessage) -> None:
        """
        チャットが来た際のデータを処理する関数
        """
        self.__dispatch(
            'message', ChatMessage(message, client=self.__client.client)
        )

    def parse_unread_messaging_message(self, message: IChatMessage) -> None:
        """
        チャットが既読になっていない場合のデータを処理する関数
        """
        self.__dispatch(
            'message', ChatMessage(message, client=self.__client.client)
        )

    def parse_notification(self, message: Dict[str, Any]) -> None:
        """
        通知イベントを解析する関数

        Parameters
        ----------
        message: Dict[str, Any]
            Received message
        """

        accept_type = ['reaction']
        notification_type = str_lower(message['type'])
        if notification_type in accept_type:
            getattr(self, f'parse_{notification_type}')(message)

    def parse_follow_request_accepted(self, message: Dict[str, Any]) -> None:
        pass

    def parse_poll_vote(self, message: Dict[str, Any]) -> None:
        pass  # TODO: 実装

    def parse_unread_notification(self, message: Dict[str, Any]) -> None:
        """
        未読の通知を解析する関数

        Parameters
        ----------
        message : Dict[str, Any]
            Received message
        """
        # notification_type = str_lower(message['type'])
        # getattr(self, f'parse_{notification_type}')(message)

    def parse_reaction(self, message: INoteReaction) -> None:
        """
        リアクションに関する情報を解析する関数
        """
        self.__dispatch(
            'reaction', NoteReaction(message),
        )

    def parse_note(self, message: INote) -> None:
        """
        ノートイベントを解析する関数
        """
        note = Note(message, self.__client.client)
        # Router(self.http.ws).capture_message(note.id) TODO: capture message
        self.__client._on_message(note)
