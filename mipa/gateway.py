from __future__ import annotations

import asyncio
import json
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, TypeVar

import aiohttp
from mipac.util import str_lower

from mipa.exception import ClientConnectorError, WebSocketReconnect

if TYPE_CHECKING:
    from .client import Client

__all__ = ('MisskeyWebSocket',)


MS = TypeVar('MS', bound='aiohttp.ClientWebSocketResponse')


class MisskeyWebSocket:
    def __init__(self, socket: MS, client: Client):
        self.socket: MS = socket
        self._dispatch = lambda *args: None
        self._connection = None
        self.client = client
        self._misskey_parsers: Optional[Dict[str, Callable[..., Any]]] = None

    @classmethod
    async def from_client(
        cls, client: Client, *, timeout: int = 60, event_name: str = 'ready'
    ):
        try:
            socket = await client.core.http.session.ws_connect(
                f'{client.url}?i={client.token}'
            )
            ws = cls(socket, client)
            ws._dispatch = client.dispatch
            ws._connection = client._connection
            ws._misskey_parsers = client._connection.parsers
            client.dispatch(event_name, socket)
            return ws
        except ClientConnectorError:
            while True:
                await asyncio.sleep(3)
                return await cls.from_client(
                    client, timeout=timeout, event_name=event_name
                )

        # await ws.poll_event(timeout=timeout)

    async def received_message(self, msg, /):
        if isinstance(msg, bytes):
            msg = msg.decode()

        self._misskey_parsers[str_lower(msg['type']).upper()](msg)

    async def poll_event(self, *, timeout: int = 60):

        msg = await self.socket.receive(timeout=timeout)

        if msg is aiohttp.http.WS_CLOSED_MESSAGE:
            await asyncio.sleep(3)
            raise WebSocketReconnect()

        elif msg.type is aiohttp.WSMsgType.TEXT:
            await self.received_message(json.loads(msg.data))
