from datetime import datetime
from typing import List


from .user import RawUser
from mipac.types import ChatPayload


class RawChat:
    """
    Attributes
    ----------
    id : str
        chat ID
    created_at : str
        chat creation time
    content : str
        chat content
    user_id : str
       ID of the user who created the chat
    author : RawUser
        user who created the chat
    recipient_id : str
    recipient : str
    group_id : str
        group ID
    file_id : str
        ID of the attached file
    is_read : bool
        whether the chat is read
    reads : List
    """

    __slots__ = (
        'id',
        'created_at',
        'content',
        'user_id',
        'author',
        'recipient_id',
        'recipient',
        'group_id',
        'file_id',
        'is_read',
        'reads',
    )

    def __init__(self, data: ChatPayload):
        """

        Parameters
        ----------
        data: ChatPayload
        """
        self.id: str = data['id']
        self.created_at: datetime = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        self.content: str = data['text']
        self.user_id: str = data['user_id']
        self.author: RawUser = RawUser(data['user'])
        self.recipient_id: str = data['recipient_id']
        self.recipient: str = data['recipient']
        self.group_id: str = data['group_id']
        self.file_id: str = data['file_id']
        self.is_read: bool = bool(data['is_read'])
        self.reads: List = data['reads']
