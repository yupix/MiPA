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

from typing import TYPE_CHECKING

from mipac import Note
from mipac.models.lite.user import LiteUser

if TYPE_CHECKING:
    from mipa.ext.commands import CMD, BotBase


class Context:
    __slots__ = ("__message", "bot", "args", "kwargs", "command", "__cmd")

    def __init__(
        self,
        *,
        message,
        bot: BotBase,
        args: tuple | None = None,
        kwargs=None,
        cmd: CMD = None,
    ):
        self.__message: Note = message
        self.bot: BotBase = bot
        self.args: tuple = args or ()
        self.kwargs = kwargs or {}
        self.command = cmd.func
        self.__cmd = cmd

    @property
    def message(self) -> Note:
        return self.__message

    @property
    def author(self) -> LiteUser:
        return self.__message.author

    @property
    def cog(self):
        return self.bot.get_cog(self.__cmd.cog_name)
