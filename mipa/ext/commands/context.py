from __future__ import annotations

from typing import TYPE_CHECKING

from mipac import Note
from mipac.models.lite.user import LiteUser

if TYPE_CHECKING:
    from mipa.ext.commands import CMD, BotBase


class Context:
    __slots__ = ('__message', 'bot', 'args', 'kwargs', 'command', '__cmd')

    def __init__(
        self, *, message, bot: BotBase, args=None, kwargs=None, cmd: CMD = None
    ):
        self.__message: Note = message
        self.bot: BotBase = bot
        self.args = args or ()
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
