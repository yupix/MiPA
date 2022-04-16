from typing import Any, Dict, Optional, TypedDict

__all__ = ('PropertiesPayload', 'FolderPayload', 'FilePayload')


class PropertiesPayload(TypedDict):
    """
    プロパティー情報
    """

    width: int
    height: int
    avg_color: Optional[str]


class FolderPayload(TypedDict):
    """
    フォルダーの情報
    """

    id: str
    created_at: str
    name: str
    folders_count: int
    files_count: int
    parent_id: str
    parent: Dict[str, Any]


class FilePayload(TypedDict):
    """
    ファイル情報
    """

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
    comment: str
    folder_id: str
    folder: FolderPayload
    user_id: str
    user: Dict[str, Any]
