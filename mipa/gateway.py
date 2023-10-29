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
import json
from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, TypeVar

import aiohttp
from aiohttp import ClientError
from mipac.utils.format import str_lower

from mipa.exception import ClientConnectorError, WebSocketReconnect
from mipa.router import Router

if TYPE_CHECKING:
    from .client import Client

__all__ = ("MisskeyWebSocket",)


MS = TypeVar("MS", bound="aiohttp.ClientWebSocketResponse")


class MisskeyWebSocket:
    def __init__(self, socket: MS, client: Client):
        self.socket: MS = socket
        self._dispatch = lambda *args: None
        self._connection = None
        self.client = client
        self._misskey_parsers: Optional[Dict[str, Callable[..., Any]]] = None

    @classmethod
    async def from_client(
        cls, client: Client, *, timeout: int = 60, event_name: str = "ready"
    ):
        try:
            socket = await client.core.http.session.ws_connect(
                f"{client.url}?i={client.token}"
            )
            ws = cls(socket, client)
            ws._dispatch = client.dispatch
            ws._connection = client._connection
            ws._misskey_parsers = client._connection.parsers
            client._router = Router(socket, max_capure=client.max_capture)
            client.dispatch(event_name, socket)
            return ws
        except (ClientConnectorError, ClientError):
            while True:
                await asyncio.sleep(3)
                return await cls.from_client(
                    client, timeout=timeout, event_name=event_name
                )

        # await ws.poll_event(timeout=timeout)

    async def received_message(self, msg, /):
        if isinstance(msg, bytes):
            msg = msg.decode()

        await self._misskey_parsers[str_lower(msg["type"]).upper()](msg)

    async def poll_event(self, *, timeout: int = 60):
        msg = await self.socket.receive(timeout=timeout)

        if msg is aiohttp.http.WS_CLOSED_MESSAGE:
            raise WebSocketReconnect()
        elif msg is aiohttp.http.WS_CLOSING_MESSAGE:
            raise WebSocketReconnect()
        elif msg.type is aiohttp.WSMsgType.TEXT:
            await self.received_message(json.loads(msg.data))
        elif msg.type is aiohttp.WSMsgType.ERROR:
            raise WebSocketReconnect()
