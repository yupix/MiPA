from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from mipac import AbstractManager, HTTPClient
from mipac.core.models.emoji import RawEmoji
from mipac.core.models.reaction import RawNoteReaction
from mipac.http import Route
from mipac.models.emoji import Emoji
from mipac.models.note import NoteReaction
from mipac.util import remove_dict_empty

if TYPE_CHECKING:
    from mipac.client import ClientActions


class ReactionManager(AbstractManager):
    def __init__(
        self,
        note_id: Optional[str] = None,
        *,
        session: HTTPClient,
        client: ClientActions
    ):
        self.__note_id: Optional[str] = note_id
        self.__session: HTTPClient = session
        self.__client: ClientActions = client

    async def add(self, reaction: str, note_id: Optional[str] = None) -> bool:
        """
        指定したnoteに指定したリアクションを付与します（内部用

        Parameters
        ----------
        reaction : Optional[str]
            付与するリアクション名
        note_id : Optional[str]
            付与対象のノートID

        Returns
        -------
        bool
            成功したならTrue,失敗ならFalse
        """
        note_id = note_id or self.__note_id

        data = remove_dict_empty({'noteId': note_id, 'reaction': reaction})
        route = Route('POST', '/api/notes/reactions/create')
        return await self.__session.request(
            route, json=data, auth=True, lower=True
        )

    async def remove(self, note_id: Optional[str] = None) -> bool:
        note_id = note_id or self.__note_id

        data = remove_dict_empty({'noteId': note_id})
        route = Route('POST', '/api/notes/reactions/delete')
        return bool(
            await self.__session.request(
                route, json=data, auth=True, lower=True
            )
        )

    async def get_reaction(
        self, reaction: str, note_id: Optional[str] = None, *, limit: int = 11
    ) -> List[NoteReaction]:
        note_id = note_id or self.__note_id
        data = remove_dict_empty(
            {'noteId': note_id, 'limit': limit, 'type': reaction}
        )
        res = await self.__session.request(
            Route('POST', '/api/notes/reactions'),
            json=data,
            auth=True,
            lower=True,
        )
        return [NoteReaction(RawNoteReaction(i)) for i in res]

    async def get_emoji_list(self) -> List[Emoji]:
        data = await self.__session.request(
            Route('GET', '/api/meta'), json={'detail': False}, auth=True
        )
        return [Emoji(RawEmoji(i)) for i in data['emojis']]
