from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from mipac import AbstractManager, HTTPClient
from mipac.http import Route

if TYPE_CHECKING:
    from mipac.client import ClientActions


class FavoriteManager(AbstractManager):
    def __init__(
        self,
        note_id: Optional[str] = None,
        *,
        session: HTTPClient,
        client: ClientActions
    ):
        self.__note_id = note_id
        self.__session: HTTPClient = session
        self.__client: ClientActions = client

    async def add(self, note_id: Optional[str] = None) -> bool:
        note_id = note_id or self.__note_id
        data = {'noteId': note_id}
        return bool(
            await self.__session.request(
                Route('POST', '/api/notes/favorites/create'),
                json=data,
                auth=True,
            )
        )

    async def remove(self, note_id: Optional[str] = None) -> bool:
        note_id = note_id or self.__note_id
        data = {'noteId': note_id}
        return bool(
            await self.__session.request(
                Route('POST', '/api/notes/favorites/delete'),
                json=data,
                auth=True,
            )
        )
