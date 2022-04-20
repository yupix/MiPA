from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from mipac.http import HTTPClient, Route
from mipac.manager.ad import AdminAdvertisingManager
from mipac.manager.admin.user import AdminUserManager
from mipac.manager.emoji import AdminEmojiManager
from mipac.manager.moderator import AdminModeratorManager

if TYPE_CHECKING:
    from mipac.client import ClientActions


class AdminActions:
    def __init__(self, session: HTTPClient, client: ClientActions):
        self.__session: HTTPClient = session
        self.__client: ClientActions = client
        self.emoji = AdminEmojiManager(session=session, client=client)
        self.user = AdminUserManager(session=session, client=client)
        self.ad = AdminAdvertisingManager(session=session, client=client)
        self.moderator = AdminModeratorManager(session=session, client=client)

    def get_emoji_instance(
        self, emoji_id: Optional[str] = None
    ) -> AdminEmojiManager:
        return AdminEmojiManager(
            emoji_id, session=self.__session, client=self.__client
        )

    async def get_invite(self) -> bool:
        return bool(
            await self.__session.request(Route('POST', '/api/admin/invite'))
        )
