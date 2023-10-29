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
import importlib
import inspect
import logging
import re
import sys
import traceback
from typing import Any, Callable, Coroutine, Dict, Optional, Tuple, Union

from aiohttp import ClientWebSocketResponse
from mipac.client import Client as API
from mipac.manager.client import ClientManager
from mipac.models.user import UserDetailed

from mipa.exception import WebSocketNotConnected, WebSocketReconnect
from mipa.gateway import MisskeyWebSocket
from mipa.router import Router
from mipa.state import ConnectionState
from mipa.utils import LOGING_LEVEL_TYPE, setup_logging

_log = logging.getLogger()


class Client:
    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        max_capture: int = 100,
        **options: Dict[Any, Any],
    ):
        super().__init__(**options)
        self.max_capture = max_capture
        self._router: Router
        self.url = None
        self.extra_events: Dict[str, Any] = {}
        self.special_events: Dict[str, Any] = {}
        self.token: Optional[str] = None
        self.origin_uri: Optional[str] = None
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.core: API
        self._connection: ConnectionState
        self.user: UserDetailed
        self.ws: Optional[MisskeyWebSocket] = None
        self.should_reconnect = True

    def _get_state(self, **options: Any) -> ConnectionState:
        return ConnectionState(
            dispatch=self.dispatch, loop=self.loop, client=self
        )

    async def on_ready(self, ws: ClientWebSocketResponse):
        """
        on_readyのデフォルト処理

        Parameters
        ----------
        ws : WebSocketClientProtocol
        """

    def event(self, name: Optional[str] = None):
        def decorator(func: Coroutine[Any, Any, Any]):
            self.add_event(func, name)
            return func

        return decorator

    def add_event(
        self, func: Coroutine[Any, Any, Any], name: Optional[str] = None
    ):
        name = func.__name__ if name is None else name
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Listeners must be coroutines")

        if name in self.extra_events:
            self.special_events[name].append(func)
        else:
            self.special_events[name] = [func]

    def listen(self, name: Optional[str] = None):
        def decorator(func: Coroutine[Any, Any, Any]):
            self.add_listener(func, name)
            return func

        return decorator

    def add_listener(
        self,
        func: Union[Coroutine[Any, Any, Any], Callable[..., Any]],
        name: Optional[str] = None,
    ):
        name = func.__name__ if name is None else name
        if not asyncio.iscoroutinefunction(func):
            raise TypeError("Listeners must be coroutines")
        _log.debug(f"add_listener: {name} {func.__name__}")
        if name in self.extra_events:
            self.extra_events[name].append(func)
        else:
            self.extra_events[name] = [func]

    def event_dispatch(
        self, event_name: str, *args: Tuple[Any], **kwargs: Dict[Any, Any]
    ) -> bool:
        """
        on_ready等といった

        Parameters
        ----------
        event_name :
        args :
        kwargs :

        Returns
        -------

        """

        ev = f"on_{event_name}"
        for event in self.special_events.get(ev, []):
            foo = importlib.import_module(event.__module__)
            coro = getattr(foo, ev)
            self.schedule_event(coro, event, *args, **kwargs)
        if ev in dir(self):
            self.schedule_event(getattr(self, ev), ev, *args, **kwargs)
        return ev in dir(self)

    def dispatch(
        self, event_name: str, *args: tuple[Any], **kwargs: Dict[Any, Any]
    ):
        ev = f"on_{event_name}"
        for event in self.extra_events.get(ev, []):
            if inspect.ismethod(event):
                coro = event
                event = event.__name__
            else:
                foo = importlib.import_module(event.__module__)
                coro = getattr(foo, ev)
            self.schedule_event(coro, event, *args, **kwargs)
        if ev in dir(self):
            self.schedule_event(getattr(self, ev), ev, *args, **kwargs)

    def schedule_event(
        self,
        coro: Callable[..., Coroutine[Any, Any, Any]],
        event_name: str,
        *args: tuple[Any],
        **kwargs: Dict[Any, Any],
    ) -> asyncio.Task[Any]:
        return self.loop.create_task(
            self._run_event(coro, event_name, *args, **kwargs),
            name=f"MiPA: {event_name}",
        )

    async def _run_event(
        self,
        coro: Callable[..., Coroutine[Any, Any, Any]],
        event_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        try:
            await coro(*args, **kwargs)
        except asyncio.CancelledError:
            pass
        except Exception:
            try:
                await self.__on_error(event_name)
            except asyncio.CancelledError:
                pass

    @staticmethod
    async def __on_error(event_method: str) -> None:
        print(f"Ignoring exception in {event_method}", file=sys.stderr)
        traceback.print_exc()

    async def on_error(self, err):
        self.event_dispatch("error", err)

    async def create_api_session(
        self,
        token: str,
        url: str,
        log_level: LOGING_LEVEL_TYPE | None,
    ) -> API:
        self.core = API(url, token, log_level=log_level)
        return self.core

    async def setup_hook(self) -> None:
        ...

    async def login(
        self, token: str, url: str, log_level: LOGING_LEVEL_TYPE | None
    ):
        """
        ユーザーにログインし、ユーザー情報を取得します

        Parameters
        ----------
        token : str
            BOTにするユーザーのTOKEN
        url : str
            BOTにするユーザーがいるインスタンスのURL
        log_level : LOGING_LEVEL_TYPE
            The log level to use for logging. Defaults to ``INFO``.
        """

        core = await self.create_api_session(token, url, log_level)
        await core.http.login()
        self.user = await core.api.get_me()
        await self.setup_hook()

    async def _connect(
        self,
        *,
        timeout: int = 60,
        event_name: str = "ready",
    ) -> None:
        self._connection = self._get_state()
        coro = MisskeyWebSocket.from_client(
            self, timeout=timeout, event_name=event_name
        )
        self.ws = await asyncio.wait_for(coro, timeout=60)
        while True:
            await self.ws.poll_event()

    async def connect(
        self,
        *,
        reconnect: bool = True,
        timeout: int = 60,
    ) -> None:
        self.should_reconnect = reconnect
        event_name = "ready"
        while True:
            try:
                await self._connect(timeout=timeout, event_name=event_name)
            except (WebSocketReconnect, asyncio.exceptions.TimeoutError):
                if not self.should_reconnect:
                    break
                event_name = "reconnect"
                await asyncio.sleep(3)

    async def disconnect(self):
        if not self.ws:
            raise WebSocketNotConnected()
        self.should_reconnect = False
        await self.ws.socket.close()

    @property
    def client(self) -> ClientManager:
        return self.core.api

    @property
    def router(self) -> Router:
        return self._router

    async def start(
        self,
        url: str,
        token: str,
        *,
        debug: bool = False,
        reconnect: bool = True,
        timeout: int = 60,
        is_ayuskey: bool = False,
        log_level: LOGING_LEVEL_TYPE | None = "INFO",
    ):
        """
        Starting Bot

        Parameters
        ----------
        url: str
            Misskey Instance Websocket URL (wss://example.com)
        token: str
            User Token
        debug: bool, default False
            debugging mode
        reconnect: bool, default True
            coming soon...
        timeout: int, default 60
            Time until websocket times out
        """
        if log_level is not None:
            setup_logging(level=log_level)
        self.token = token
        url = url[:-1] if url[-1] == "/" else url
        split_url = url.split("/")

        if origin_url := re.search(r"wss?://(.*)", url):
            origin_url = (
                origin_url.group(0)
                .replace("wss", "https")
                .replace("ws", "http")
                .replace("/streaming", "")
            )
        else:
            origin_url = url
        if "streaming" not in split_url:
            split_url.append("streaming")
            url = "/".join(split_url)
        self.url = url.replace("https", "wss").replace("http", "ws")
        self.origin_url = origin_url
        await self.login(token, origin_url, log_level)
        await self.connect(reconnect=reconnect, timeout=timeout)
