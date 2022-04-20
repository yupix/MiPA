from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from mipac.core.models.chat import RawChat
from mipac.exception import ParameterError
from mipac.http import HTTPClient, Route
from mipac.models.chat import Chat
from mipac.util import check_multi_arg

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions


class ChatManager:
    def __init__(
        self,
        session: HTTPClient,
        client: ClientActions,
        user_id: Optional[str] = None,
        message_id: Optional[str] = None,
    ):
        self.__session: HTTPClient = session
        self.__client: ClientActions = client
        self.__user_id = user_id
        self.__message_id = message_id

    async def get_history(self, limit: int = 100, group: bool = True):
        """
        Get the chat history.

        Parameters
        ----------
        limit : int, default=100, max=100
            Number of items to retrieve, up to 100
        group : bool, default=True
            Whether to include group chat or not

        Returns
        -------
        list[Chat]
            List of chat history
        """

        if limit > 100:
            raise ParameterError('limit must be greater than 100')

        args = {'limit': limit, 'group': group}
        data = await self.__session.request(
            Route('POST', '/api/messaging/history'), json=args, auth=True
        )
        return [Chat(RawChat(d)) for d in data]

    async def send(
        self,
        text: Optional[str] = None,
        *,
        file_id: Optional[str] = None,
        user_id: Optional[str] = None,
        group_id: Optional[str] = None,
    ) -> Chat:
        """
        Send chat.

        Parameters
        ----------
        text : Optional[str], default=None
            チャットのテキスト
        file_id : Optional[str], default=None
            添付するファイルのID
        user_id : Optional[str], default=None
            送信するユーザーのID
        group_id : Optional[str], default=None
            送信するグループのID
        """
        user_id = user_id or self.__user_id
        data = {
            'userId': user_id,
            'groupId': group_id,
            'text': text,
            'fileId': file_id,
        }
        res = await self.__session.request(
            Route('POST', '/api/messaging/messages/create'),
            json=data,
            auth=True,
            lower=True,
        )
        return Chat(RawChat(res))

    async def delete(self, message_id: Optional[str] = None) -> bool:
        """
        指定したidのメッセージを削除します。

        Parameters
        ----------
        message_id : str
            メッセージid

        Returns
        -------
        bool
            成功したか否か
        """

        if check_multi_arg(message_id, self.__message_id) is False:
            raise ParameterError('message_idがありません')

        message_id = message_id or self.__message_id
        args = {'messageId': f'{message_id}'}
        data = await self.__session.request(
            Route('POST', '/api/messaging/messages/delete'),
            json=args,
            auth=True,
        )
        return bool(data)
