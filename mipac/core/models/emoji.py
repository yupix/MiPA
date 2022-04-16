from typing import List, Optional

from mipac.types import EmojiPayload


class RawEmoji:
    """
    Attributes
    ----------
    id : Optional[str]
        絵文字のID
    aliases : Optional[List[str]]
        絵文字のエイリアス
    name : Optional[str]
        絵文字の名前
    category : Optional[str]
        絵文字のカテゴリ
    host : Optional[str]
        絵文字のホスト
    url : Optional[str]
        絵文字のURL
    """

    __slots__ = ('id', 'aliases', 'name', 'category', 'host', 'url')

    def __init__(self, data: EmojiPayload):
        self.id: Optional[str] = data.get('id')
        self.aliases: Optional[List[str]] = data.get('aliases')
        self.name: Optional[str] = data.get('name')
        self.category: Optional[str] = data.get('category')
        self.host: Optional[str] = data.get('host')
        self.url: Optional[str] = data.get('url')
