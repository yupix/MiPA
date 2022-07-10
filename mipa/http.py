"""MiPAのWebSocket部分"""

import json
import sys
from typing import Any, Optional
from mipa.exception import ClientConnectorError

import aiohttp

from mipa import __version__

__all__ = ('HTTPClient', 'HTTPSession')


class _MissingSentinel:
    def __eq__(self, other):
        return False

    def __bool__(self):
        return False

    def __repr__(self):
        return '...'


MISSING: Any = _MissingSentinel()


async def json_or_text(response: aiohttp.ClientResponse):
    text = await response.text(encoding='utf-8')
    try:
        if 'application/json' in response.headers['Content-Type']:
            return json.loads(text)
    except KeyError:
        pass


class HTTPClient:
    def __init__(self) -> None:
        self.__session: aiohttp.ClientSession = MISSING
        self.token: Optional[str] = None
        user_agent = 'Misskey Bot (https://github.com/yupix/MiPA {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
        self.user_agent = user_agent.format(
            __version__, sys.version_info, aiohttp.__version__
        )

    async def close_session(self):
        await self.__session.close()

    async def ws_connect(self, url: str, *, compress: int = 0) -> Any:
        kwargs = {
            'autoclose': False,
            'max_msg_size': 0,
            'timeout': 30.0,
            'headers': {'User-Agent': self.user_agent},
            'compress': compress,
        }
        try:
            ws = await self.__session.ws_connect(url, **kwargs)
        except aiohttp.client_exceptions.ClientConnectorError:
            raise ClientConnectorError()
        return ws


HTTPSession: HTTPClient = HTTPClient()
