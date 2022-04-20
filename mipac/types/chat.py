from __future__ import annotations

from typing import TYPE_CHECKING, List, TypedDict

if TYPE_CHECKING:
    from mipac.types import UserPayload

__all__ = ('ChatPayload',)


class ChatPayload(TypedDict):
    id: str
    created_at: str
    text: str
    user_id: str
    user: UserPayload
    recipient_id: str
    recipient: str
    group_id: str
    file_id: str
    is_read: bool
    reads: List
