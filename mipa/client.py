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
from mipac.manager import ClientActions
from mipac.models.user import UserDetailed

from mipa.exception import WebSocketReconnect
from mipa.gateway import MisskeyWebSocket
from mipa.state import ConnectionState
from mipa.utils import LOGING_LEVEL_TYPE, setup_logging

_log = logging.getLogger()


class Client:
    def __init__(
        self,
        loop: Optional[asyncio.AbstractEventLoop] = None,
        **options: Dict[Any, Any],
    ):
        super().__init__(**options)
        self.url = None
        self.extra_events: Dict[str, Any] = {}
        self.special_events: Dict[str, Any] = {}
        self.token: Optional[str] = None
        self.origin_uri: Optional[str] = None
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.core: API
        self._connection: ConnectionState
        self.user: UserDetailed
        self.ws: MisskeyWebSocket

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
            raise TypeError('Listeners must be coroutines')

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
            raise TypeError('Listeners must be coroutines')
        _log.debug(f'add_listener: {name} {func.__name__}')
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

        ev = f'on_{event_name}'
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
        ev = f'on_{event_name}'
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
            name=f'MiPA: {event_name}',
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
        print(f'Ignoring exception in {event_method}', file=sys.stderr)
        traceback.print_exc()

    async def on_error(self, err):
        self.event_dispatch('error', err)

    async def create_api_session(self, token: str, url: str) -> API:
        self.core = API(url, token)
        return self.core

    async def login(self, token: str, url: str):
        """
        ユーザーにログインし、ユーザー情報を取得します
        
        Parameters
        ----------
        token : str
            BOTにするユーザーのTOKEN
        url : str
            BOTにするユーザーがいるインスタンスのURL
        """

        core = await self.create_api_session(token, url)
        await core.http.login()
        self.user = await core.api.get_me()

    async def connect(
        self,
        *,
        reconnect: bool = True,
        timeout: int = 60,
        event_name: str = 'ready',
    ) -> None:
        self._connection = self._get_state()
        coro = MisskeyWebSocket.from_client(
            self, timeout=timeout, event_name=event_name
        )
        try:
            self.ws = await asyncio.wait_for(coro, timeout=60)
        except asyncio.exceptions.TimeoutError:
            await self.connect(reconnect=reconnect, timeout=timeout)

        while True:
            try:
                await self.ws.poll_event()
            except WebSocketReconnect:
                await self.connect(event_name='reconnect')

    @property
    def client(self) -> ClientActions:
        return self.core.api

    async def start(
        self,
        url: str,
        token: str,
        *,
        debug: bool = False,
        reconnect: bool = True,
        timeout: int = 60,
        is_ayuskey: bool = False,
        log_level: LOGING_LEVEL_TYPE = 'INFO',
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
        setup_logging(level=log_level)
        self.token = token
        if origin_url := re.search(r'wss?://(.*)/streaming', url):
            origin_url = (
                origin_url.group(0)
                .replace('wss', 'https')
                .replace('ws', 'http')
                .replace('/streaming', '')
            )
        else:
            origin_url = url
        self.origin_url = origin_url[:-1] if url[-1] == '/' else origin_url
        self.url = url
        await self.login(token, origin_url)
        await self.connect(reconnect=reconnect, timeout=timeout)
