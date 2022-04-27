from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, ClassVar, Dict, List, Optional, Tuple

from mipa.ext.commands._types import _BaseCommand
from mipa.ext.commands.core import Command

if TYPE_CHECKING:
    from mipa.ext import Bot


class CogMeta(type):
    __cog_name__: str

    def __new__(cls, *args: Tuple[Any], **kwargs: Dict[str, Any]):
        name, bases, attrs = args
        attrs['__cog_name__'] = kwargs.pop('name', name)
        attrs['__cog_settings__'] = kwargs.pop('command_attrs', {})
        listeners = {}
        commands = {}
        no_bot_cog = 'Commands or listeners must not start with cog_ or bot_ (in method {0.__name__}.{1})'
        new_cls = super().__new__(cls, name, bases, attrs, **kwargs)

        for base in reversed(new_cls.__mro__):  # 多重継承を確認 !コマンドを登録
            for elem, value in base.__dict__.items():
                if elem in commands:
                    del commands[elem]  # commandsから削除
                if elem in listeners:
                    del listeners[elem]  # listenersから削除
                is_static_method = isinstance(value, staticmethod)

                if isinstance(value, Command):
                    commands[elem] = value

                if is_static_method:  # staticmethodか確認
                    value = value.__func__  #
                # 関数をvalueに !valueが重要
                if isinstance(value, _BaseCommand):
                    commands[elem] = value
                elif inspect.iscoroutinefunction(value):
                    try:
                        value.__cog_listener__
                    except AttributeError:
                        continue
                    else:
                        if elem.startswith(('cog', 'bot_')):
                            raise TypeError(no_bot_cog.format(base, elem))
                        listeners[elem] = value
        new_cls.__cog_commands__ = list(commands.values())

        listeners_as_list: List[tuple[str, Any]] = []
        for listener in listeners.values():
            for listener_name in listener.__cog_listener_names__:
                listeners_as_list.append((listener_name, listener))

        new_cls.__cog_listeners__ = listeners_as_list
        return new_cls

    def __init__(self, *args: Tuple[Any], **kwargs: Dict[str, Any]):
        super().__init__(*args, **kwargs)

    @classmethod
    def qualified_name(cls) -> str:
        return cls.__cog_name__


class Cog(metaclass=CogMeta):
    __cog_name__ = ClassVar[str]
    __cog_settings__: Dict[str, Any] = {}
    __cog_listeners__: ClassVar[List[Tuple[str, str]]]
    __cog_commands__: List[Command] = []

    def __new__(cls, *args: tuple[Any], **kwargs: Dict[str, Any]):
        self = super().__new__(cls)
        self.__cog_commands__ = tuple(cls.__cog_commands__)
        return self

    @classmethod
    def listener(cls, name: Optional[str] = None):
        def decorator(func: Cog):
            actual = func
            if isinstance(actual, staticmethod):
                actual = actual.__func__
            if not inspect.iscoroutinefunction(actual):
                raise TypeError(
                    'Listener function must be a coroutine function.'
                )
            actual.__cog_listener__ = True
            to_assign = name or actual.__name__
            try:
                actual.__cog_listener_names__.append(to_assign)
            except AttributeError:
                actual.__cog_listener_names__ = [to_assign]
            return func

        return decorator

    @classmethod
    def qualified_name(cls) -> str:
        return cls.__cog_name__

    def _inject(self, bot: Bot):
        for command in self.__cog_commands__:
            bot.add_command(command, self.__cog_name__)

        for name, method_func in self.__cog_listeners__:
            bot.add_listener(getattr(self, name), name)

        return self
