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
import functools
from typing import TYPE_CHECKING, List, Optional

from mipa.ext.commands._types import _BaseCommand

if TYPE_CHECKING:
    from mipa.ext.commands import Context


def hooked_wrapped_callback(coro):
    @functools.wraps(coro)
    async def wrapped(*args, **kwargs):
        ret = await coro(*args, **kwargs)
        return ret

    return wrapped


class CMD:
    def __init__(
        self, cmd_type: str, key: str, func: "Command", cog_name: str
    ):
        self.cmd_type = cmd_type
        self.key = key
        self.func = func
        self.cog_name = cog_name


class CommandManager:
    def __init__(self, *args, **kwargs):
        self.all_commands: List[CMD] = []
        super().__init__(*args, **kwargs)  # Clientクラスを初期化する

    def add_command(self, command: "Command", cog_name: str):
        if not isinstance(command, Command):
            raise TypeError(f"{command}はCommandクラスである必要があります")
        command_type = "regex" if command.regex else "text"
        command_key = command.regex or command.text
        self.all_commands.append(
            CMD(command_type, command_key, command, cog_name)
        )


class Command(_BaseCommand):
    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        return self

    def __init__(self, func, regex: str, text: str, **kwargs):
        if not asyncio.iscoroutinefunction(func):
            raise TypeError(f"{func}はコルーチンでなければなりません")
        self.regex: str = regex
        self.text: str = text
        self.callback = func
        self.cog = None

    @property
    def qualified_name(self) -> str:
        return self.regex or self.text

    def __str__(self):
        return self.qualified_name

    @staticmethod
    async def _parse_arguments(ctx: Context):
        args = (ctx,) if ctx.cog is None else (ctx.cog, ctx)
        ctx.args = args + ctx.args
        return ctx

    async def invoke(self, ctx: Context, *args, **kwargs):
        ctx = await self._parse_arguments(ctx)
        await self.callback(*ctx.args, **ctx.kwargs)


def mention_command(regex: Optional[str] = None, text: Optional[str] = None):
    def decorator(func, **kwargs):
        return Command(func, regex=regex, text=text, **kwargs)

    return decorator
