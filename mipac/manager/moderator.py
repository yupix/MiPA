from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from mipac import AbstractManager
from mipac.http import HTTPClient, Route

if TYPE_CHECKING:
    from mipac.client import ClientActions


class AdminModeratorManager(AbstractManager):
    def __init__(
        self,
        user_id: Optional[str] = None,
        *,
        session: HTTPClient,
        client: ClientActions
    ):
        self.__user_id: Optional[str] = user_id
        self.__session: HTTPClient = session
        self.__client: ClientActions = client

    async def add(self, user_id: Optional[str] = None) -> bool:
        """
        Add a user as a moderator

        Parameters
        ----------
        user_id : Optional[str], default=None
            ユーザーのID

        Returns
        -------
        bool
            成功したか否か
        """

        user_id = user_id or self.__user_id
        data = {'userId': user_id}
        res = await self.__session.request(
            Route('POST', '/api/moderators/add'),
            json=data,
            auth=True,
            lower=True,
        )
        return bool(res)

    async def remove(self, user_id: Optional[str] = None) -> bool:
        """
        Unmoderate a user

        Parameters
        ----------
        user_id : Optional[str], default=None
            ユーザーのID

        Returns
        -------
        bool
            成功したか否か
        """
        user_id = user_id or self.__user_id
        data = {'userId': user_id}
        res = await self.__session.request(
            Route('POST', '/api/moderators/remove'),
            json=data,
            auth=True,
            lower=True,
        )
        return bool(res)
