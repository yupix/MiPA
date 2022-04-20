from __future__ import annotations

import json
import sys
from typing import Any, Dict

import aiohttp

from mipac import __version__
from mipac.exception import APIError
from mipac.util import remove_dict_empty, upper_to_lower


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


class Route:
    def __init__(self, method: str, path: str):
        self.path: str = path
        self.method: str = method
        # self.url = config.i.origin_uri + path


class HTTPClient:
    def __init__(self, url: str, token: str) -> None:
        user_agent = 'Misskey Bot (https://github.com/yupix/Mi.py {0}) Python/{1[0]}.{1[1]} aiohttp/{2}'
        self.user_agent = user_agent.format(
            __version__, sys.version_info, aiohttp.__version__
        )
        self.__session: aiohttp.ClientSession = MISSING
        self.__url: str = url
        self.__token: str = token

    async def request(self, route: Route, **kwargs):
        headers: Dict[str, str] = {
            'User-Agent': self.user_agent,
        }

        is_lower = kwargs.pop('lower') if kwargs.get('lower') else False

        if 'json' in kwargs:
            headers['Content-Type'] = 'application/json'
            kwargs['json'] = kwargs.pop('json')

        if kwargs.get('auth') and kwargs.pop('auth'):
            key = 'json' if 'json' in kwargs or 'data' not in kwargs else 'data'
            if not kwargs.get(key):
                kwargs[key] = {}
            kwargs[key]['i'] = self.__token

        for i in ('json', 'data'):
            if kwargs.get(i):
                kwargs[i] = remove_dict_empty(kwargs[i])

        async with self.__session.request(
            route.method, self.__url + route.path, **kwargs
        ) as res:
            data = await json_or_text(res)
            if is_lower:
                if isinstance(data, list):
                    data = [upper_to_lower(i) for i in data]
                else:
                    data = upper_to_lower(data)
            if 300 > res.status >= 200:
                return data
            if 511 > res.status >= 300:
                raise APIError(data)

    async def close_session(self):
        await self.__session.close()

    async def login(self):
        self.__session = aiohttp.ClientSession()
        data = await self.request(Route('POST', '/api/i'), auth=True)
        return data
