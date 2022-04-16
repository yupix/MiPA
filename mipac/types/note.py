from typing import Any, Dict, List, Optional, TypedDict

from .drive import FilePayload
from .emoji import EmojiPayload
from .user import UserPayload

__all__ = ('NotePayload', 'GeoPayload', 'ReactionPayload', 'PollPayload', 'RenotePayload', 'OptionalReaction')


class GeoPayload(TypedDict):
    """
    衛星情報
    """
    coordinates: Optional[List[Any]]
    altitude: Optional[int]
    accuracy: Optional[int]
    altitude_accuracy: Optional[int]
    heading: Optional[int]
    speed: Optional[int]


class PollPayload(TypedDict, total=False):
    """
    アンケート情報
    """

    multiple: bool
    expires_at: int
    choices: List[str]
    expired_after: int


class RenotePayload(TypedDict):
    id: str
    created_at: str
    user_id: str
    user: UserPayload
    text: str
    cw: str
    visibility: str
    renote_count: int
    replies_count: Optional[int]
    reactions: Dict[str, Any]
    emojis: Optional[List]
    file_ids: Optional[List]
    files: Optional[List]
    reply_id: Optional[str]
    renote_id: Optional[str]
    uri: Optional[str]
    poll: Optional[PollPayload]
    tags: Optional[List[str]]
    channel_id: Optional[str]


class _NoteOptional(TypedDict, total=False):
    """
    ノートに必ず存在すると限らない物
    """
    text: str
    cw: str
    geo: GeoPayload


class NotePayload(_NoteOptional):
    """
    note object
    """

    id: str
    created_at: str
    user_id: str
    user: UserPayload
    visibility: Optional[str]
    renote_count: Optional[int]
    replies_count: Optional[int]
    reactions: Dict[str, Any]
    emojis: List[EmojiPayload]
    file_ids: Optional[List[str]]
    files: Optional[List[FilePayload]]
    reply_id: Optional[str]
    renote_id: Optional[str]
    poll: Optional[PollPayload]
    visible_user_ids: Optional[List[str]]
    via_mobile: Optional[bool]
    local_only: Optional[bool]
    extract_mentions: Optional[bool]
    extract_hashtags: Optional[bool]
    extract_emojis: Optional[bool]
    preview: Optional[bool]
    media_ids: Optional[List[str]]
    renote: Optional[RenotePayload]
    field: Optional[dict]
    tags: Optional[List[str]]
    channel_id: Optional[str]


class OptionalReaction(TypedDict, total=False):
    created_at: str
    type: str
    is_read: bool
    user: UserPayload
    note: NotePayload
    id: str


class ReactionPayload(OptionalReaction):
    reaction: str
