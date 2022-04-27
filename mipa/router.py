"""Misskeyのチャンネルへの接続や、メッセージのキャプチャ等のWebSocket関連"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Iterable, Literal

if TYPE_CHECKING:
    from aiohttp.client_ws import ClientWebSocketResponse

__all__ = ['Router']


class Router:
    """
    Attributes
    ----------
    web_socket : ClientWebSocketResponse
        WebSocketクライアント

    Methods
    -------
    channels:
        与えられたlistを元にチャンネルに接続します
    global_time_line:
        WebSocketでGlobalTimeLineに接続します
    main_channel:
        WebSocketでMainチャンネルに接続します
    home_time_line:
        WebSocketでHomeTimeLineに接続します
    local_time_line:
        WebSocketでLocalTimeLineに接続します
    capture_message:
        与えられたメッセージを元にnote idを取得し、そのメッセージをon_message等の監視対象に追加します
    """

    def __init__(self, web_socket: ClientWebSocketResponse):
        self.web_socket: ClientWebSocketResponse = web_socket

    async def connect_channel(
        self,
        channel_list: Iterable[Literal['global', 'main', 'home', 'local']],
    ) -> None:
        """
        与えられたlistを元にチャンネルに接続します

        Parameters
        ----------
        channel_list : Iterable[Literal['global', 'main', 'home', 'local']]
            ['global', 'local', 'home', 'main']
        """

        channel_dict = {
            'global': 'globalTimeline',
            'main': 'main',
            'home': 'homeTimeline',
            'local': 'localTimeline',
        }
        try:
            for channel in channel_list:
                get_channel = channel_dict[channel]
                await self.web_socket.send_json(
                    {
                        'type': 'connect',
                        'body': {
                            'channel': f'{get_channel}',
                            'id': f'{uuid.uuid4()}',
                        },
                    }
                )

        except KeyError:
            pass

    async def capture_message(self, message_id: str) -> None:
        """
        与えられたメッセージを元にnote idを取得し、そのメッセージをon_message等の監視対象に追加します

        Parameters
        ----------
        message_id : str
        """

        await self.web_socket.send_json(
            {'type': 'subNote', 'body': {'id': f'{message_id}'}}
        )
