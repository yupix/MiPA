from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from mipac.core import RawUser
from mipac.models.emoji import Emoji
from mipac.models.instance import Instance
from mipac.types import (ChannelPayload, FieldContentPayload,
                         PinnedNotePayload, PinnedPagePayload)

if TYPE_CHECKING:
    from mipac.actions.user import UserActions
    from mipac.manager.client import ClientActions


__all__ = ['User', 'FollowRequest', 'Followee']


class Followee:
    def __init__(self, data, *, client: ClientActions):
        self.id: str = data['id']
        self.created_at: datetime = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        )
        self.followee_id: str = data['followee_id']
        self.follower_id: str = data['follower_id']
        self.user: User = User(RawUser(data['follower']), client=client)


class FollowRequest:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['username']
        self.nickname = data['name']
        self.host = data['host']
        self.avatar_url = data['avatar_url']
        self.avatar_blurhash = data['avatar_blurhash']
        self.avatar_color = data['avatar_color']
        self.emojis = data['emojis']
        self.online_status = data['online_status']
        self.is_admin: bool = bool(data.get('is_admin'))
        self.is_bot: bool = bool(data.get('is_bot'))
        self.is_cat: bool = bool(data.get('is_cat'))
        # self.__client = manager.ClientActions()

    # @property
    # def action(self) -> FollowRequestManager:
    #     return self.__client.user.get_follow_request(self.id)

    # async def get_profile(self) -> User:
    #     return await self.__client.user.get(user_id=self.id)


class Channel:
    def __init__(self, data: ChannelPayload):
        self.id: Optional[str] = data.get('id')
        self.created_at: Optional[datetime] = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        ) if data.get('created_at') else None
        self.last_noted_at: Optional[str] = data.get('last_noted_at')
        self.name: Optional[str] = data.get('name')
        self.description: Optional[str] = data.get('description')
        self.banner_url: Optional[str] = data.get('banner_url')
        self.notes_count: Optional[int] = data.get('notes_count')
        self.users_count: Optional[int] = data.get('users_count')
        self.is_following: Optional[bool] = data.get('is_following')
        self.user_id: Optional[str] = data.get('user_id')


class PinnedNote:
    def __init__(self, data: PinnedNotePayload, *, client: ClientActions):
        self.id: Optional[str] = data.get('id')
        self.created_at: Optional[datetime] = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        ) if data.get('created_at') else None
        self.text: Optional[str] = data.get('text')
        self.cw: Optional[str] = data.get('cw')
        self.user_id: Optional[str] = data.get('user_id')
        self.user: Optional[User] = User(
            RawUser(data['user']), client=client
        ) if data.get('user') else None
        self.reply_id: Optional[str] = data.get('reply_id')
        self.reply: Optional[Dict[str, Any]] = data.get('reply')
        self.renote: Optional[Dict[str, Any]] = data.get('renote')
        self.via_mobile: Optional[bool] = data.get('via_mobile')
        self.is_hidden: Optional[bool] = data.get('is_hidden')
        self.visibility: Optional[bool] = bool(data['visibility']) if data.get(
            'visibility'
        ) else None
        self.mentions: Optional[List[str]] = data.get('mentions')
        self.visible_user_ids: Optional[List[str]] = data.get(
            'visible_user_ids'
        )
        self.file_ids: Optional[List[str]] = data.get('file_ids')
        self.files: Optional[List[str]] = data.get('files')
        self.tags: Optional[List[str]] = data.get('tags')
        self.poll: Optional[List[str]] = data.get('poll')
        self.channel: Optional[Channel] = Channel(data['channel']) if data.get(
            'channel'
        ) else None
        self.local_only: Optional[bool] = data.get('local_only')
        self.emojis: Optional[List[Emoji]] = [
            Emoji(i) for i in data['emojis']
        ] if data.get('emojis') else None
        self.reactions: Optional[Dict[str, Any]] = data.get('reactions')
        self.renote_count: Optional[int] = data.get('renote_count')
        self.replies_count: Optional[int] = data.get('replies_count')
        self.uri: Optional[str] = data.get('uri')
        self.url: Optional[str] = data.get('url')
        self.my_reaction: Optional[Dict[str, Any]] = data.get('my_reaction')


class PinnedPage:
    def __init__(self, data: PinnedPagePayload):
        self.id: Optional[str] = data.get('id')
        self.created_at: Optional[datetime] = datetime.strptime(
            data['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'
        ) if data.get('created_at') else None
        self.updated_at: Optional[str] = data.get('updated_at', None)
        self.title: Optional[str] = data.get('title')
        self.name: Optional[str] = data.get('name')
        self.summary: Optional[str] = data.get('summary')
        self.content: Optional[List] = data.get('content')
        self.variables: Optional[List] = data.get('variables')
        self.user_id: Optional[str] = data.get('user_id')
        self.author: Optional[Dict[str, Any]] = data.get('author')


class FieldContent:
    def __init__(self, data: FieldContentPayload):
        self.name: str = data['name']
        self.value: str = data['value']


class User:
    def __init__(self, raw_user: RawUser, *, client: ClientActions):
        self.__raw_user = raw_user
        self.__client: ClientActions = client

    @property
    def id(self):
        return self.__raw_user.id

    @property
    def name(self):
        return self.__raw_user.name

    @property
    def nickname(self):
        return self.__raw_user.nickname

    @property
    def host(self):
        return self.__raw_user.host

    @property
    def avatar_url(self):
        return self.__raw_user.avatar_url

    @property
    def is_admin(self):
        return self.__raw_user.is_admin

    @property
    def is_moderator(self):
        return self.__raw_user.is_moderator

    @property
    def is_bot(self):
        return self.__raw_user.is_bot

    @property
    def is_cat(self):
        return self.__raw_user.is_cat

    @property
    def is_lady(self):
        return self.__raw_user.is_lady

    @property
    def emojis(self):
        return self.__raw_user.emojis

    @property
    def online_status(self):
        return self.__raw_user.online_status

    @property
    def url(self):
        return self.__raw_user.url

    @property
    def uri(self):
        return self.__raw_user.uri

    @property
    def created_at(self) -> datetime:
        return self.__raw_user.created_at

    @property
    def updated_at(self):
        return self.__raw_user.updated_at

    @property
    def is_locked(self):
        return self.__raw_user.is_locked

    @property
    def is_silenced(self):
        return self.__raw_user.is_silenced

    @property
    def is_suspended(self):
        return self.__raw_user.is_suspended

    @property
    def description(self):
        return self.__raw_user.description

    @property
    def location(self):
        return self.__raw_user.location

    @property
    def birthday(self):
        return self.__raw_user.birthday

    @property
    def fields(self):
        return self.__raw_user.fields

    @property
    def followers_count(self):
        return self.__raw_user.followers_count

    @property
    def following_count(self):
        return self.__raw_user.following_count

    @property
    def notes_count(self):
        return self.__raw_user.notes_count

    @property
    def pinned_note_ids(self):
        return self.__raw_user.pinned_note_ids

    @property
    def pinned_notes(self):
        return self.__raw_user.pinned_notes

    @property
    def pinned_page_id(self):
        return self.__raw_user.pinned_page_id

    @property
    def pinned_page(self):
        return self.__raw_user.pinned_page

    @property
    def ff_visibility(self):
        return self.__raw_user.ff_visibility

    @property
    def is_following(self):
        return self.__raw_user.is_following

    @property
    def is_follow(self):
        return self.__raw_user.is_follow

    @property
    def is_blocking(self):
        return self.__raw_user.is_blocking

    @property
    def is_blocked(self):
        return self.__raw_user.is_blocked

    @property
    def is_muted(self):
        return self.__raw_user.is_muted

    @property
    def details(self):
        return self.__raw_user.details

    @property
    def instance(self) -> Union[Instance, None]:
        return (
            Instance(self.__raw_user.instance, client=self.__client)
            if self.__raw_user.instance
            else None
        )

    @property
    def action(self) -> UserActions:
        return self.__client._create_user_instance(self).action
