from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from mipac import AbstractManager, HTTPClient
from mipac.http import Route

if TYPE_CHECKING:
    from mipac.client import ClientActions


class PagesManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientActions):
        self.__session: HTTPClient = session
        self.__client: ClientActions = client

    async def get_pages(
        self,
        limit: int = 100,
        since_id: Optional[int] = None,
        until_id: Optional[int] = None,
    ):
        data = {'limit': limit, 'since_id': since_id, 'until_id': until_id}
        res = await self.__session.request(
            Route('POST', '/api/i/pages'), json=data, auth=True
        )
