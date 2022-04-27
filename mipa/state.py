from __future__ import annotations

import asyncio
import inspect
from typing import TYPE_CHECKING, Any, Callable, Dict

from mipac.core.models import RawChat, RawNote, RawReaction, RawUser
from mipac.models import Chat, Emoji, FollowRequest, Note, Reaction, User
from mipac.types import ChatPayload, NotePayload, UserPayload
from mipac.util import str_lower, upper_to_lower

if TYPE_CHECKING:
    from mipa.client import Client


class ConnectionState:
    def __init__(
        self,
        dispatch: Callable[..., Any],
        loop: asyncio.AbstractEventLoop,
        client: Client,
    ):
        self.__client: Client = client
        self.__dispatch = dispatch
        # self.logger = get_module_logger(__name__) TODO: 直す
        self.loop: asyncio.AbstractEventLoop = loop
        self.parsers = parsers = {}
        for attr, func in inspect.getmembers(self):
            if attr.startswith('parse'):
                parsers[attr[6:].upper()] = func

    def parse_emoji_added(self, message: Dict[str, Any]):
        self.__dispatch('emoji_add', Emoji(message['body']['emoji']))

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
        # self.logger.debug(f'ChannelType: {channel_type}') TODO: 修正
        # self.logger.debug(f'recv event type: {channel_type}') TODO: 修正
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

        self.__dispatch('follow_request', FollowRequest(message))

    def parse_me_updated(self, message: UserPayload):
        self.__dispatch(
            'me_updated', User(RawUser(message), client=self.__client.action)
        )

    def parse_read_all_announcements(self, message: Dict[str, Any]) -> None:
        pass  # TODO: 実装

    def parse_reply(self, message: NotePayload) -> None:
        """
        リプライ
        """
        self.__dispatch(
            'message', Note(RawNote(message), client=self.__client.action)
        )

    def parse_follow(self, message: Dict[str, Any]) -> None:
        """
        ユーザーをフォローした際のイベントを解析する関数
        """

        self.__dispatch(
            'user_follow', User(RawUser(message), client=self.__client.action)
        )

    def parse_followed(self, message: Dict[str, Any]) -> None:
        """
        フォローイベントを解析する関数
        """

        self.__dispatch(
            'follow', User(RawUser(message), client=self.__client.action)
        )

    def parse_mention(self, message: Dict[str, Any]) -> None:
        """
        メンションイベントを解析する関数
        """

        self.__dispatch(
            'mention', Note(RawNote(message), client=self.__client.action)
        )

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

    def parse_messaging_message(self, message: ChatPayload) -> None:
        """
        チャットが来た際のデータを処理する関数
        """
        self.__dispatch(
            'message', Chat(RawChat(message), client=self.__client.action)
        )

    def parse_unread_messaging_message(self, message: Dict[str, Any]) -> None:
        """
        チャットが既読になっていない場合のデータを処理する関数
        """
        self.__dispatch(
            'message', Chat(RawChat(message), client=self.__client.action)
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

    def parse_reaction(self, message: Dict[str, Any]) -> None:
        """
        リアクションに関する情報を解析する関数
        """
        self.__dispatch(
            'reaction',
            Reaction(RawReaction(message), client=self.__client.action),
        )

    def parse_note(self, message: NotePayload) -> None:
        """
        ノートイベントを解析する関数
        """
        note = Note(RawNote(message), self.__client.action)
        # Router(self.http.ws).capture_message(note.id) TODO: capture message
        self.__client._on_message(note)
