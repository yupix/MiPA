from datetime import datetime
from typing import Any, Dict, Optional

from mipac.types import FilePayload, FolderPayload, PropertiesPayload


class RawProperties:
    """
    Attributes
    ----------
    width : int
        ファイルの幅
    height : int
        ファイルの高さ
    avg_color : Optional[str]
        ファイルの平均色
    """

    __slots__ = ('width', 'height', 'avg_color')

    def __init__(self, data: PropertiesPayload):
        self.width: Optional[int] = data.get('width')
        self.height: int = data['height']
        self.avg_color: Optional[str] = data.get('avg_color')


class RawFolder:
    """
    Attributes
    ----------
    id : str
        フォルダーのID
    created_at : datetime
        フォルダーの作成された日時
    name : str
        フォルダーの名前
    folders_count : Optional[int]
        # TODO: 調査
    parent_id : str
        親フォルダーのID
    parent : Optional[Dict[str, Any]]
        親フォルダー
    """

    __slots__ = ('id', 'created_at', 'name', 'folders_count', 'parent_id', 'parent')

    def __init__(self, data: FolderPayload):
        self.id: str = data['id']
        self.created_at: datetime = datetime.strptime(data["created_at"], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.name: str = data['name']
        self.folders_count: Optional[int] = data.get('folders_count', 0)
        self.parent_id: str = data['parent_id']
        self.parent: Optional[Dict[str, Any]] = data.get('parent')


class RawFile:
    """
    Attributes
    ----------
    id : str
        ファイルのID
    created_at : datetime
        ファイルのの作成された日時
    name : str
        ファイルの名前
    type : str
        ファイルの拡張子
    md5 : str
        ファイルのmd5
    size : int
        ファイルのサイズ
    is_sensitive : bool
        このファイルはセンシティブか否か
    blurhash : str
        このファイルのblurhash
    properties : Optional[RawProperties]
        ファイルの情報
    url : str
        ファイルのurl
    thumbnail_url : str
        ファイルのサムネイルurl
    comment : str
        ファイルのコメント
    folder_id : str
        親フォルダのID
    folder : Optional[RawFolder]
        親フォルダの情報？
        # TODO: 調査
    user_id : str
        ファイル作成者のID
    user : Dict[str, Any]
        ファイル作成者の情報
    """

    __slots__ = (
        'id', 'created_at', 'name', 'type', 'md5', 'size', 'is_sensitive', 'blurhash', 'properties', 'url', 'thumbnail_url',
        'comment', 'folder_id', 'folder', 'user_id', 'user'
    )

    def __init__(self, data: FilePayload):
        self.id: str = data['id']
        self.created_at: datetime = datetime.strptime(data["created_at"], '%Y-%m-%dT%H:%M:%S.%fZ')
        self.name: str = data['name']
        self.type: str = data['type']
        self.md5: str = data['md5']
        self.size: int = data['size']
        self.is_sensitive: bool = data['is_sensitive']
        self.blurhash: str = data['blurhash']
        self.properties: Optional[RawProperties] = RawProperties(data['properties']) if len(data.get('properties')) else None
        self.url: str = data['url']
        self.thumbnail_url: str = data['thumbnail_url']
        self.comment: str = data['comment']
        self.folder_id: str = data['folder_id']
        self.folder: Optional[RawFolder] = RawFolder(data['folder']) if data.get('folder') else None
        self.user_id: str = data['user_id']
        self.user: Dict[str, Any] = data['user']
