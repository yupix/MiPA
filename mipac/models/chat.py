from __future__ import annotations


__all__ = ['Chat']

from mipac.core.models.chat import RawChat


class Chat:
    """
    チャットオブジェクト
    """

    def __init__(self, raw_data: RawChat):
        self.__raw_data = raw_data

    @property
    def id(self):
        return self.__raw_data.id

    @property
    def created_at(self):
        return self.__raw_data.created_at

    @property
    def content(self):
        return self.__raw_data.content

    @property
    def user_id(self):
        return self.__raw_data.user_id

    @property
    def author(self):
        return self.__raw_data.author

    @property
    def recipient_id(self):
        return self.__raw_data.recipient_id

    @property
    def recipient(self):
        return self.__raw_data.recipient

    @property
    def group_id(self):
        return self.__raw_data.group_id

    @property
    def file_id(self):
        return self.__raw_data.file_id

    @property
    def is_read(self):
        return self.__raw_data.is_read

    @property
    def reads(self):
        return self.__raw_data.reads

    async def delete(self) -> bool:
        """
        チャットを削除します（チャットの作者である必要があります）

        Returns
        -------
        bool:
            成功したか否か
        """
        res = await manager.ClientActions().chat.delete(message_id=self.id)
        return bool(res)
