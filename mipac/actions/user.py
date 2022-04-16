from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

from aiocache import Cache, cached

from mipac.core import RawUser
from mipac.core.models.note import RawNote
from mipac.exception import NotExistRequiredData, ParameterError
from mipac.http import HTTPClient, Route
from mipac.manager.note import NoteManager
from mipac.models.note import Note
from mipac.models.user import User
from mipac.util import check_multi_arg, get_cache_key, key_builder, remove_dict_empty

__all__ = ['UserActions']

if TYPE_CHECKING:
    from mipac.manager.client import ClientActions


class UserActions:
    def __init__(
            self,
            session: HTTPClient,
            client: ClientActions,
            user: Optional[User] = None
    ):
        self.__session: HTTPClient = session
        self.__user: User = user
        self.__client: ClientActions = client
        self.note: NoteManager(session=session, client=client)

    @cached(ttl=10, namespace='get_user', key_builder=key_builder)
    async def get(self, user_id: Optional[str] = None, username: Optional[str] = None, host: Optional[str] = None) -> User:
        """
        ユーザーのプロフィールを取得します。一度のみサーバーにアクセスしキャッシュをその後は使います。
        fetch_userを使った場合はキャッシュが廃棄され再度サーバーにアクセスします。

        Parameters
        ----------
        user_id : str
            取得したいユーザーのユーザーID
        username : str
            取得したいユーザーのユーザー名
        host : str, default=None
            取得したいユーザーがいるインスタンスのhost

        Returns
        -------
        User
            ユーザー情報
        """

        field = remove_dict_empty({"userId": user_id, "username": username, "host": host})
        data = await self.__session.request(Route('POST', '/api/users/show'), json=field, auth=True, lower=True)
        return User(RawUser(data), client=self.__client)

    @get_cache_key
    async def fetch(self, user_id: Optional[str] = None, username: Optional[str] = None,
                    host: Optional[str] = None, **kwargs) -> User:
        """
        サーバーにアクセスし、ユーザーのプロフィールを取得します。基本的には get_userをお使いください。

        Parameters
        ----------
        user_id : str
            取得したいユーザーのユーザーID
        username : str
            取得したいユーザーのユーザー名
        host : str, default=None
            取得したいユーザーがいるインスタンスのhost

        Returns
        -------
        User
            ユーザー情報
        """
        if not check_multi_arg(user_id, username):
            raise ParameterError("user_id, usernameどちらかは必須です")

        field = remove_dict_empty({"userId": user_id, "username": username, "host": host})
        data = await self.__session.request(Route('POST', '/api/users/show'), json=field, auth=True, lower=True)
        old_cache = Cache(namespace='get_user')
        await old_cache.delete(kwargs['cache_key'].format('get_user'))
        return User(RawUser(data), client=self.__client)

    async def get_notes(
            self,
            user_id: Optional[str] = None,
            include_replies: bool = True,
            limit: int = 10,
            since_id: Optional[str] = None,
            until_id: Optional[str] = None,
            since_date: int = 0,
            until_date: int = 0,
            include_my_renotes: bool = True,
            with_files: bool = False,
            file_type: Optional[List[str]] = None,
            exclude_nsfw: bool = True
    ) -> List[Note]:
        user_id = user_id or self.__user.id
        data = {
            'userId': user_id,
            'includeReplies': include_replies,
            'limit': limit,
            'sinceId': since_id,
            'untilId': until_id,
            'sinceDate': since_date,
            'untilDate': until_date,
            'includeMyRenotes': include_my_renotes,
            'withFiles': with_files,
            'fileType': file_type,
            'excludeNsfw': exclude_nsfw
        }
        res = await self.__session.request(Route('POST', '/api/users/notes'), json=data, auth=True, lower=True)
        return [Note(RawNote(i), client=self.__client) for i in res]

    def get_mention(self, user: Optional[User] = None) -> str:
        """
        Get mention name of user.
        
        Parameters
        ----------
        user : Optional[User], default=None
            メンションを取得したいユーザーのオブジェクト
        
        Returns
        -------
        str
            メンション
        """

        user = user or self.__user

        if user is None:
            raise NotExistRequiredData('Required parameters: user')
        return f'@{user.name}@{user.host}' if user.instance else f'@{user.name}'

    # def get_follow(self, user_id: str) -> FollowManager:
    #     return FollowManager(user_id=user_id)
    #
    # def get_follow_request(self, user_id: str) -> FollowRequestManager:
    #     return FollowRequestManager(user_id=user_id)
