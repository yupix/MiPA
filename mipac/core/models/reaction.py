from datetime import datetime

__all__ = ['RawNoteReaction']

from mipac.types import NoteReactionPayload, UserPayload


class RawNoteReaction:
    """
    Attributes
    ----------
    id : str
        TODO: 調査
    created_at : datetime
        リアクションが付けられた時間
    user : UserPayload
        リアクションを付けたユーザー
    reaction : str
    """

    __slots__ = ('id', 'created_at', 'user', 'reaction')

    def __init__(self, data: NoteReactionPayload):
        self.id: str = data['id']
        self.created_at: datetime = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        self.user: UserPayload = data['user']
        self.reaction: str = data['type']
