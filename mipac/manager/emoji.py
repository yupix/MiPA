from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from mipac import AbstractManager
from mipac.exception import NotExistRequiredData
from mipac.http import HTTPClient, Route
from mipac.util import check_multi_arg

if TYPE_CHECKING:
    from mipac.client import ClientActions


class AdminEmojiManager(AbstractManager):
    def __init__(
        self,
        emoji_id: Optional[str] = None,
        *,
        session: HTTPClient,
        client: ClientActions
    ):
        self.emoji_id: Optional[str] = emoji_id
        self.__session: HTTPClient = session
        self.__client: ClientActions = client

    async def add(
        self,
        file_id: Optional[str] = None,
        *,
        name: Optional[str] = None,
        url: Optional[str] = None,
        category: Optional[str] = None,
        aliases: Optional[List[str]] = None
    ) -> bool:
        if config.is_ayuskey:  # TODO: どうにかする
            data = {
                'name': name,
                'url': url,
                'category': category,
                'aliases': aliases,
            }
        else:
            data = {'fileId': file_id}

        if not check_multi_arg(file_id, url):
            raise NotExistRequiredData('required a file_id or url')
        return bool(
            await self.__session.request(
                Route('POST', '/api/admin/emoji/add'),
                json=data,
                lower=True,
                auth=True,
            )
        )

    async def remove(self, emoji_id: Optional[str] = None) -> bool:
        emoji_id = emoji_id or self.emoji_id

        if emoji_id is None:
            raise NotExistRequiredData('idが不足しています')

        return bool(
            await self.__session.request(
                Route('POST', '/api/admin/emoji/remove'),
                json={'id': emoji_id},
                lower=True,
                auth=True,
            )
        )
