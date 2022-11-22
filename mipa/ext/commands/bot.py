"""Commands FrameWork用のCore部分"""

from __future__ import annotations

import asyncio
import importlib
import inspect
import re
import sys
import traceback
from types import ModuleType
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    Dict,
    List,
    Optional,
    Tuple,
    Union,
)

from mipac.models.user import UserDetailed

from mipa import Client
from mipa.ext.commands.context import Context
from mipa.ext.commands.core import CommandManager
from mipa.exception import (
    CogNameDuplicate,
    ExtensionAlreadyLoaded,
    ExtensionFailed,
    InvalidCogPath,
    NoEntryPointError,
)

if TYPE_CHECKING:
    from aiohttp.client_ws import ClientWebSocketResponse
    from mipa.ext import Cog


__all__ = ['BotBase', 'Bot']


class BotBase(CommandManager):
    def __init__(self, **options: Dict[Any, Any]):
        super().__init__(**options)
        self.extra_events: Dict[str, Any] = {}
        self.special_events: Dict[str, Any] = {}
        self._check_once: List[Any] = []  # TODO: いつか確認する
        self._checks: List[Any] = []  # TODO: いつか確認する
        self._after_invoke = None
        self.token: Optional[str] = None
        self.origin_uri: Optional[str] = None
        self.__extensions: Dict[str, Any] = {}
        self.user: UserDetailed
        self.__cogs: Dict[str, Cog] = {}
        self.strip_after_prefix = options.get('strip_after_prefix', False)
        # self.logger = get_module_logger(__name__) TODO: 直す
        self.loop = asyncio.get_event_loop()

    def _on_message(self, message):
        self.dispatch('message', message)

    async def on_ready(self, ws: ClientWebSocketResponse):
        """
        on_readyのデフォルト処理

        Parameters
        ----------
        ws : ClientWebSocketResponse
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

        if name in self.extra_events:
            self.extra_events[name].append(func)
        else:
            self.extra_events[name] = [func]

    async def event_dispatch(
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
            await self.schedule_event(coro, event, *args, **kwargs)
        if ev in dir(self):
            await self.schedule_event(getattr(self, ev), ev, *args, **kwargs)
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

    def add_cog(self, cog: Cog, override: bool = False) -> None:
        cog_name = cog.__cog_name__
        existing = self.__cogs.get(cog_name)
        if existing is not None:
            if not override:
                raise CogNameDuplicate()
            self.remove_cog(cog_name)  # TODO: 作る

        cog = cog._inject(self)
        self.__cogs[cog_name] = cog

    def remove_cog(self, name: str):  # TODO: Optional[Cog]を返すように
        """Cogを削除します"""
        cog = self.__cogs.get(name)
        if cog is None:
            return

        cog._eject(self)

        return cog

    def _load_from_module(self, spec: ModuleType, key: str) -> None:
        try:
            setup = spec.setup
        except AttributeError as e:
            raise NoEntryPointError(f'{key} にsetupが存在しません') from e

        try:
            setup(self)
        except Exception as e:
            raise ExtensionFailed(key, e) from e
        else:
            self.__extensions[key] = spec

    @staticmethod
    def _resolve_name(name: str, package: Optional[str]) -> str:
        try:
            return importlib.util.resolve_name(name, package)
        except ImportError as e:
            raise InvalidCogPath(name) from e

    def load_extension(
        self, name: str, *, package: Optional[str] = None
    ) -> None:
        """拡張をロードする

        Parameters
        ----------
        name : str
            [description]
        package : Optional[str], optional
            [description], by default None
        """
        name = self._resolve_name(name, package)
        if name in self.__extensions:
            raise ExtensionAlreadyLoaded
        try:
            module = importlib.import_module(name)
        except ModuleNotFoundError as e:
            raise InvalidCogPath(f'cog: {name} へのパスが無効です') from e
        self._load_from_module(module, name)

    def schedule_event(
        self,
        coro: Callable[..., Coroutine[Any, Any, Any]],
        event_name: str,
        *args: tuple[Any],
        **kwargs: Dict[Any, Any],
    ) -> asyncio.Task[Any]:
        return asyncio.create_task(
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
        await self.event_dispatch('error', err)

    def get_cog(self, name: str) -> Optional[str]:
        return self.__cogs.get(name)

    async def get_context(self, message, cmd, cls=Context) -> Context:
        return cls(message=message, bot=self, cmd=cmd)

    async def progress_command(self, message):
        for cmd in self.all_commands:
            ctx = await self.get_context(message, cmd)
            if cmd.cmd_type == 'regex':
                if re.search(cmd.key, message.content):
                    hit_list = re.findall(cmd.key, message.content)
                    if isinstance(hit_list[0], tuple):
                        hit_list = tuple(
                            i for i in hit_list[0] if len(i.rstrip()) > 0
                        )
                    ctx.args = hit_list
                    await cmd.func.invoke(ctx)
            elif message.content.find(cmd.key) != -1:
                await cmd.func.invoke(ctx)
            else:
                continue

    async def on_mention(self, message):
        await self.progress_command(message)


class Bot(Client, BotBase):
    pass
