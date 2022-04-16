from typing import Any, Dict, List, Optional, TypedDict

from .drive import FilePayload
from .emoji import EmojiPayload
from .instance import InstancePayload

__all__ = ('ChannelPayload', 'FieldContentPayload', 'UserPayload', 'PinnedPagePayload', 'PinnedNotePayload', 'OptionalUser')


class ChannelPayload(TypedDict):
    id: Optional[str]
    created_at: Optional[str]
    last_noted_at: Optional[str]
    name: Optional[str]
    description: Optional[str]
    banner_url: Optional[str]
    notes_count: Optional[int]
    users_count: Optional[int]
    is_following: Optional[bool]
    user_id: Optional[str]


class PinnedNotePayload(TypedDict):
    id: Optional[str]
    created_at: Optional[str]
    text: Optional[str]
    cw: Optional[str]
    user_id: Optional[str]
    user: Optional['UserPayload']
    reply_id: Optional[str]
    renote_id: Optional[str]
    reply: Optional[Dict[str, Any]]
    renote: Optional[Dict[str, Any]]
    via_mobile: Optional[bool]
    is_hidden: Optional[bool]
    visibility: Optional[str]
    mentions: Optional[List[str]]
    visible_user_ids: Optional[List[str]]
    file_ids: Optional[List[str]]
    files: Optional[List[FilePayload]]
    tags: Optional[List[str]]
    poll: Optional[Dict[str, Any]]
    channel_id: Optional[str]
    channel: Optional[ChannelPayload]
    local_only: Optional[bool]
    emojis: Optional[List[EmojiPayload]]
    reactions: Optional[Dict[str, Any]]
    renote_count: Optional[int]
    replies_count: Optional[int]
    uri: Optional[str]
    url: Optional[str]
    my_reaction: Optional[Dict[str, Any]]


class PinnedPagePayload(TypedDict):
    id: Optional[str]
    created_at: Optional[str]
    updated_at: Optional[str]
    title: Optional[str]
    name: Optional[str]
    summary: Optional[str]
    content: Optional[List]
    variables: Optional[List]
    user_id: Optional[str]
    author: Optional[Dict[str, Any]]


class FieldContentPayload(TypedDict):
    name: str
    value: str


class OptionalUser(TypedDict, total=False):
    user_id: str
    name: str
    host: str
    is_admin: bool
    is_moderator: bool
    is_bot: bool
    is_cat: bool
    is_lady: bool
    online_status: str


class UserPayload(OptionalUser):
    id: str
    username: str
    avatar_url: Optional[str]
    avatar_blurhash: Optional[str]
    avatar_color: Optional[str]
    emojis: Optional[List[str]]
    url: str
    uri: str
    created_at: str
    updated_at: str
    is_locked: bool
    is_silenced: bool
    is_suspended: bool
    description: str
    location: str
    birthday: str
    fields: Any
    followers_count: int
    following_count: int
    notes_count: int
    pinned_note_ids: List[str]
    pinned_notes: List[str]
    pinned_page_id: str
    pinned_page: str
    ff_visibility: str
    is_following: bool
    is_follow: bool
    is_blocking: bool
    is_blocked: bool
    is_muted: bool
    instance: Optional[InstancePayload]
