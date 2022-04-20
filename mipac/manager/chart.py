from __future__ import annotations

from typing import TYPE_CHECKING

from mipac import AbstractManager
from mipac.core.models.chart import RawActiveUsersChart, RawDriveChart
from mipac.http import HTTPClient, Route

if TYPE_CHECKING:
    from mipac.client import ClientActions

__all__ = ('ChartManager',)


class ChartManager(AbstractManager):
    def __init__(self, *, session: HTTPClient, client: ClientActions):
        self.__session: HTTPClient = session
        self.__client: ClientActions = client

    async def get_active_user(
        self, span: str = 'day', limit: int = 30, offset: int = 0
    ) -> RawActiveUsersChart:
        data = {'span': span, 'limit': limit, 'offset': offset}
        data = await self.__session.request(
            Route('POST', '/api/charts/active-users'),
            json=data,
            auth=True,
            lower=True,
        )
        return RawActiveUsersChart(data)

    async def get_drive(
        self, span: str = 'day', limit: int = 30, offset: int = 0
    ) -> RawDriveChart:
        data = {'span': span, 'limit': limit, 'offset': offset}
        data = await self.__session.request(
            Route('POST', '/api/charts/drive'),
            json=data,
            auth=True,
            lower=True,
        )
        return RawDriveChart(data)
