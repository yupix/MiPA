from datetime import datetime
from typing import List, Optional

__all__ = ('RawUserDetails', 'RawUser')

from mipac.core.models.instance import RawInstance
from mipac.types import UserPayload


class RawUserDetails:
    """
    ユーザー情報だが、一般的に使うか怪しいもの

    Attributes
    ----------
    avatar_blurhash: Optional[str]
        ユーザーのアバターのblurhash
    avatar_color: str
        ユーザーのアバターの色
    lang: str
        ユーザーの言語
    """

    __slots__ = (
        'avatar_blurhash',
        'avatar_color',
        'banner_url',
        'banner_blurhash',
        'banner_color',
        'two_factor_enabled',
        'use_password_less_login',
        'security_keys',
        'has_pending_follow_request_from_you',
        'has_pending_follow_request_to_you',
        'public_reactions',
        'lang',
    )

    def __init__(self, data):
        self.avatar_blurhash: Optional[str] = data.get('avatar_blurhash')
        self.avatar_color: Optional[str] = data.get('avatar_color')
        self.banner_url = data.get('banner_url')
        self.banner_blurhash = data.get('banner_blurhash')
        self.banner_color = data.get('banner_color')
        self.two_factor_enabled = data.get('two_factor_enabled', False)
        self.use_password_less_login = data.get('use_password_less_login', False)
        self.security_keys = data.get('security_keys', False)
        self.has_pending_follow_request_from_you = data.get(
            'has_pending_follow_request_from_you', False
        )
        self.has_pending_follow_request_to_you = data.get(
            'has_pending_follow_request_to_you', False
        )
        self.public_reactions = data.get('public_reactions', False)
        self.lang = data.get('lang')


class RawUser:
    """
    id : str
        ユーザーのID
    name : str
        ユーザーの名前
    nickname : Optional[str]
        ユーザーの表示名
    host : Optional[str]
        # TODO: いい感じに
    avatar_url : Optional[str]
        ユーザーのアバターurl
    is_admin : bool
        管理者か否か
    is_bot : bool
        ボットか否か
    is_cat : bool
        ねこか否か
    is_lady : bool
        お嬢様か否か (Ayuskeyのみ)
    emojis : Optional[List[str]]
        # TODO 謎
    url : Optional[str]
        # TODO 謎
    uri : Optional[str]
        # TODO 謎
    created_at : Optional[datetime]
        ユーザーの作成日時
    ff_visibility : str
        # TODO 謎
    is_following : bool
        フォローされてるか否か
    is_follow : bool
        フォローしているか否か
    is_blocking : bool
        ブロックしているか否か
    is_blocked : bool
        ブロックされてるか否か
    is_muted : bool
        ミュートしているか否か
    details : RawUserDetails
        ユーザーの詳細情報
    instance : Optional[RawInstance]
        インスタンスの情報
    """

    __slots__ = (
        'id',
        'name',
        'nickname',
        'host',
        'avatar_url',
        'is_admin',
        'is_moderator',
        'is_bot',
        'is_cat',
        'is_lady',
        'emojis',
        'online_status',
        'url',
        'uri',
        'created_at',
        'updated_at',
        'is_locked',
        'is_silenced',
        'is_suspended',
        'description',
        'location',
        'birthday',
        'fields',
        'followers_count',
        'following_count',
        'notes_count',
        'pinned_note_ids',
        'pinned_notes',
        'pinned_page_id',
        'pinned_page',
        'ff_visibility',
        'is_following',
        'is_follow',
        'is_blocking',
        'is_blocked',
        'is_muted',
        'details',
        'instance',
    )

    def __init__(self, data: UserPayload):
        self.id: str = data['user_id'] if data.get('user_id') else data['id']
        self.name: str = data['username']
        self.nickname: Optional[str] = data.get('name')
        self.host: Optional[str] = data.get('host')
        self.avatar_url: Optional[str] = data.get('avatar_url')
        self.is_admin: bool = bool(data.get('is_admin'))
        self.is_moderator: bool = bool(data.get('is_moderator'))
        self.is_bot: bool = bool(data.get('is_bot'))
        self.is_cat: bool = bool(data.get('is_cat', False))
        self.is_lady: bool = bool(data.get('is_lady', False))
        self.emojis: Optional[List[str]] = data.get('emojis')
        self.online_status = data.get('online_status', None)
        self.url: Optional[str] = data.get('url')
        self.uri: Optional[str] = data.get('uri')
        self.created_at: Optional[datetime] = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        ) if data.get('created_at') else None
        self.updated_at = data.get('updated_at')
        self.is_locked = data.get('is_locked', False)
        self.is_silenced = data.get('is_silenced', False)
        self.is_suspended = data.get('is_suspended', False)
        self.description = data.get('description')
        self.location = data.get('location')
        self.birthday = data.get('birthday')
        self.fields = data.get('fields', [])
        self.followers_count = data.get('followers_count', 0)
        self.following_count = data.get('following_count', 0)
        self.notes_count = data.get('notes_count', 0)
        self.pinned_note_ids = data.get('pinned_note_ids', [])
        self.pinned_notes = data.get('pinned_notes', [])
        self.pinned_page_id = data.get('pinned_page_id')
        self.pinned_page = data.get('pinned_page')
        self.ff_visibility: str = data.get('ff_visibility', 'public')
        self.is_following: bool = bool(data.get('is_following', False))
        self.is_follow: bool = bool(data.get('is_follow', False))
        self.is_blocking: bool = bool(data.get('is_blocking', False))
        self.is_blocked: bool = bool(data.get('is_blocked', False))
        self.is_muted: bool = bool(data.get('is_muted', False))
        self.details: RawUserDetails = RawUserDetails(data)
        self.instance: Optional[RawInstance] = RawInstance(
            data['instance']
        ) if data.get('instance') else None
