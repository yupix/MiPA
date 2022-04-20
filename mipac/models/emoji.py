from __future__ import annotations

__all__ = ('Emoji',)

from mipac.core.models.emoji import RawEmoji


class Emoji:
    def __init__(self, raw_data: RawEmoji):
        self.__raw_data = raw_data

    @property
    def id(self):
        return self.__raw_data.id

    @property
    def aliases(self):
        return self.__raw_data.aliases

    @property
    def name(self):
        return self.__raw_data.name

    @property
    def category(self):
        return self.__raw_data.category

    @property
    def host(self):
        return self.__raw_data.host

    @property
    def url(self):
        return self.__raw_data.url

    # @property
    # def action(self):
    #     return mi.framework.manager.ClientActions().emoji
