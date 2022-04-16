from datetime import datetime
from typing import Any, Dict, List, Optional

from mipac.core import RawUser
from mipac.core.models.drive import RawFile
from mipac.core.models.emoji import RawEmoji
from mipac.core.models.poll import RawPoll
from mipac.types import NotePayload, ReactionPayload, RenotePayload
from mipac.util import upper_to_lower


class RawRenote:
    """
    Attributes
    ----------
    id : str
    created_at : datetime
    user_id :str
    user : RawUser
    content: Optional[str], default=None
    cw : Optional[str], default=None
    visibility : str
    renote_count : int
    replies_count : int
    reactions
    emojis
    file_ids : List[str]
    files
    reply_id
    renote_id
    uri
    poll Optional[RawPoll]
    """

    __slots__ = ('id', 'created_at', 'user_id', 'user', 'content', 'cw', 'visibility', 'renote_count', 'replies_count',
                 'replies_count', 'reactions', 'emojis', 'file_ids', 'files', 'reply_id', 'renote_id', 'uri', 'poll')

    def __init__(self, data: RenotePayload):
        self.id: str = data["id"]
        self.created_at: datetime = datetime.strptime(data["created_at"], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.user_id: str = data["user_id"]
        self.user: RawUser = RawUser(data['user'])
        self.content: Optional[str] = data.get("text", None)
        self.cw: Optional[str] = data["cw"]
        self.visibility: str = data["visibility"]
        self.renote_count: int = data["renote_count"]
        self.replies_count: int = data["replies_count"]
        self.reactions = data["reactions"]  # TODO:型探す
        self.emojis = data["emojis"]  # TODO:型探す
        self.file_ids: List[str] = data["file_ids"]
        self.files = data["files"]
        self.reply_id = data["reply_id"]
        self.files = data["files"]
        self.reply_id = data["reply_id"]
        self.renote_id = data["renote_id"]
        self.uri = data.get("uri")
        self.poll: Optional[RawPoll] = RawPoll(data["poll"]) if data.get("poll") else None


class RawReaction:
    """
    Attributes
    ----------
    id : Optional[str], default=None
    created_at : Optional[datetime], default=None
    type : Optional[str], default=None
    is_read : bool
    user : Optional[RawUser], default=None
    note : Optional[RawNote], default=None
    reaction : str
    """

    __slots__ = ('id', 'created_at', 'type', 'is_read', 'user', 'note', 'reaction')

    def __init__(self, data: ReactionPayload):
        self.id: Optional[str] = data.get('id')
        self.created_at: Optional[str] = datetime.strptime(data["created_at"], '%Y-%m-%dT%H:%M:%S.%fZ') if data.get(
            'created_at') else None
        self.type: Optional[str] = data.get('type')
        self.is_read: bool = bool(data.get('is_read'))
        self.user: Optional[RawUser] = RawUser(data['user']) if data.get('user') else None
        self.note: Optional[RawNote] = RawNote(data['note']) if data.get('note') else None
        self.reaction: str = data['reaction']


class RawNote:
    """
    Attributes
    ----------
    id :  str
    created_at :  datetime
    user_id :  str
    author :  RawUser
    content : Optional[str]
    cw : Optional[str]
    renote : Optional[RawRenote]
    visibility : Optional[str]
    renote_count : Optional[int]
    replies_count : Optional[int]
    reactions : Optional[Dict[str, Any]]
    emojis : List[RawEmoji]
    file_ids : Optional[List[str]]
    files : List[RawFile]
    reply_id : Optional[str]
    renote_id : Optional[str]
    poll : Optional[RawPoll]
    visible_user_ids : Optional[List[str]]
    via_mobile :  bool
    local_only :  bool
    extract_mentions :  bool
    extract_hashtags :  bool
    extract_emojis :  bool
    preview :  bool
    media_ids : Optional[List[str]]
    field : Optional[dict]
    tags : Optional[List[str]]
    channel_id : Optional[str]
    """

    __slots__ = (
        'id', 'created_at', 'user_id', 'author', 'content', 'cw', 'renote', 'visibility', 'renote_count', 'replies_count',
        'reactions', 'emojis', 'file_ids', 'files', 'reply_id', 'renote_id', 'uri', 'poll', 'visible_user_ids',
        'via_mobile', 'local_only', 'extract_mentions', 'extract_hashtags', 'extract_emojis', 'preview', 'media_ids',
        'field', 'tags', 'channel_id')

    def __init__(self, data: NotePayload):
        self.id: str = data["id"]
        self.created_at: datetime = datetime.strptime(data["created_at"], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.user_id: str = data["user_id"]
        self.author: RawUser = RawUser(data['user'])
        self.content: Optional[str] = data.get("text")
        self.cw: Optional[str] = data.get("cw")
        self.renote: Optional[RawRenote] = RawRenote(data['renote']) if data.get('renote') else None
        self.visibility: Optional[str] = data.get("visibility")  # This may be an optional
        self.renote_count: Optional[int] = data.get("renote_count")  # TODO: Optionalかどうか
        self.replies_count: Optional[int] = data.get("replies_count")  # TODO: Optionalかどうか
        self.reactions: Dict[str, Any] = data["reactions"]
        self.emojis: List[RawEmoji] = [RawEmoji(i) for i in data["emojis"]]
        self.file_ids: Optional[List[str]] = data["file_ids"]
        self.files: List[RawFile] = [RawFile(upper_to_lower(i)) for i in data["files"]]
        self.reply_id: Optional[str] = data["reply_id"]
        self.renote_id: Optional[str] = data["renote_id"]
        self.poll: Optional[RawPoll] = RawPoll(data["poll"]) if data.get("poll") else None
        self.visible_user_ids: Optional[List[str]] = data.get("visible_user_ids", [])
        self.via_mobile: bool = bool(data.get("via_mobile", False))
        self.local_only: bool = bool(data.get("local_only", False))
        self.extract_mentions: bool = bool(data.get("extract_mentions"))
        self.extract_hashtags: bool = bool(data.get("extract_hashtags"))
        self.extract_emojis: bool = bool(data.get("extract_emojis"))
        self.preview: bool = bool(data.get("preview"))
        self.media_ids: Optional[List[str]] = data.get("media_ids")
        self.field: Optional[dict] = {}
        self.tags: Optional[List[str]] = data.get("tags", [])
        self.channel_id: Optional[str] = data.get("channel_id")
