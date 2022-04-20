from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, TypedDict

if TYPE_CHECKING:
    from mipac.types import PropertiesPayload, UserPayload


class PageContentPayload(TypedDict):
    id: str
    type: str
    text: Optional[str]
    file_id: Optional[str]
    width: Optional[int]
    height: Optional[int]
    note: Optional[str]
    detailed: Optional[bool]
    fn: Optional[Any]
    var: Optional[Any]
    event: Optional[Any]
    action: Optional[str]
    content: Optional[str]
    message: Optional[Any]
    primary: Optional[bool]
    inc: Optional[int]
    canvas_id: Optional[str]
    attach_canvas_image: Optional[bool]
    default: Optional[str]
    value: Optional[List[Any]]

    children: Optional['PageContentPayload']


class VariablePayload(TypedDict):
    id: str
    name: str
    type: str
    value: Optional[str]


class PageFilePayload(TypedDict):
    id: str
    created_at: str
    name: str
    type: str
    md5: str
    size: int
    is_sensitive: bool
    blurhash: str
    properties: PropertiesPayload
    url: str
    thumbnail_url: str
    comment: Optional[str]
    folder_id: Optional[str]
    folder: Any
    user_id: str
    user: Any


class EyeCatchingImagePayload(PageFilePayload):
    pass


class AttachedFilePayload(PageFilePayload):
    pass


class PagePayload(TypedDict):
    id: str
    created_at: str
    updated_at: str
    user_id: str
    user: UserPayload
    content: List[PageContentPayload]
    variable: List[VariablePayload]
    title: str
    name: str
    summary: Optional[str]
    hide_title_when_pinned: bool
    align_center: bool
    font: str
    script: str
    eye_catching_image_id: Optional[str]
    eye_catching_image: EyeCatchingImagePayload
    attached_files: List[AttachedFilePayload]
    liked_count: int
