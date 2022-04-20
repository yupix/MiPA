from __future__ import annotations
from typing import Optional, TYPE_CHECKING

from mipac.core import RawUser
from mipac.exception import NotSupportedError
from mipac.http import HTTPClient, Route
from mipac.models.user import User

if TYPE_CHECKING:
    from mipac.client import ClientActions


class AdminUserManager:
    def __init__(
        self,
        user_id: Optional[str] = None,
        *,
        session: HTTPClient,
        client: ClientActions
    ):
        self.__user_id = user_id
        self.__session: HTTPClient = session
        self.__client: ClientActions = client

    async def create_account(self, username: str, password: str) -> User:
        """
        Create a new account.

        Parameters
        ----------
        username : str
            User's name
        password : str
            User's password

        Returns
        -------
        User
            Created user
        """

        if config.is_ayuskey:
            raise NotSupportedError('Ayuskeyではサポートされていません')
        data = {'username': username, 'password': password}
        res = await self.__session.request(
            Route('POST', '/api/admin/accounts/create'),
            json=data,
            auth=True,
            lower=True,
        )
        return User(RawUser(res), client=self.__client)

    async def delete_account(self, user_id: Optional[str] = None) -> bool:
        """
        Deletes the user with the specified user ID.

        Parameters
        ----------
        user_id : Optional[str], default=None
            ID of the user to be deleted
        Returns
        -------
        bool
            Success or failure
        """

        user_id = user_id or self.__user_id

        data = {'userId': user_id}
        res = await self.__session.request(
            Route('POST', '/api/admin/accounts/delete'),
            json=data,
            auth=True,
            lower=True,
        )
        return bool(res)

    async def show_user(self, user_id: Optional[str] = None) -> User:
        """
        Shows the user with the specified user ID.

        Parameters
        ----------
        user_id : Optional[str], default=None
            ID of the user to be shown

        Returns
        -------
        User
        """

        user_id = user_id or self.__user_id
        data = {'userId': user_id}
        res = await self.__session.request(
            Route('GET', '/api/admin/show-user'), json=data, auth=True, lower=True
        )
        return User(RawUser(res), client=self.__client)

    async def suspend(self, user_id: Optional[str] = None) -> bool:
        """
        Suspends the user with the specified user ID.

        Parameters
        ----------
        user_id : Optional[str], default=None
            ID of the user to be suspended

        Returns
        -------
        bool
            Success or failure
        """

        user_id = user_id or self.__user_id
        data = {'userId': user_id}
        res = await self.__session.request(
            Route('POST', '/api/admin/suspend-user'), json=data, auth=True, lower=True
        )
        return bool(res)

    async def unsuspend(self, user_id: Optional[str] = None) -> bool:
        """
        Unsuspends the user with the specified user ID.

        Parameters
        ----------
        user_id : Optional[str], default=None
            ID of the user to be unsuspended

        Returns
        -------
        bool
            Success or failure
        """

        user_id = user_id or self.__user_id
        data = {'userId': user_id}
        res = await self.__session.request(
            Route('POST', '/api/admin/unsuspend-user'), json=data, auth=True, lower=True
        )
        return bool(res)
