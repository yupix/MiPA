from __future__ import annotations
from typing import TYPE_CHECKING

from mipac.actions.admin import AdminActions
from mipac.http import HTTPClient
from mipac.manager.chart import ChartManager
from mipac.manager.chat import ChatManager
from mipac.manager.drive import DriveManager
from mipac.manager.note import NoteManager
from mipac.manager.reaction import ReactionManager
from mipac.manager.user import UserManager

if TYPE_CHECKING:
    from mipac.models.user import User


class ClientActions:
    def __init__(self, session: HTTPClient):
        self.__session: HTTPClient = session
        self.note: NoteManager = NoteManager(session=session, client=self)
        self.chat: ChatManager = ChatManager(session=session, client=self)
        self.user: UserManager = UserManager(session=session, client=self)
        self.admin: AdminActions = AdminActions(session=session, client=self)  # TODO: 作る
        self.drive: DriveManager = DriveManager(session=session, client=self)  # TODO: 作る
        self.reaction: ReactionManager = ReactionManager(session=session, client=self)  # TODO: 作る
        self.chart: ChartManager = ChartManager(session=session, client=self)  # TODO: 作る

    def _create_user_instance(self, user: User) -> UserManager:
        return UserManager(session=self.__session, client=self, user=user)

    def _create_note_instance(self, note_id: str) -> NoteManager:
        return NoteManager(note_id, session=self.__session, client=self)
