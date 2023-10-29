"""
The MIT License (MIT)

Copyright (c) 2015-present Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

The Software is modified as follows:
    - Delete unused functions and method.
    - Removing functions beyond what is necessary to make it work.
    - Simplification of some functions.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import json
import sys
from typing import Any, Optional

import aiohttp

from mipa import __version__
from mipa.exception import ClientConnectorError
from mipa.utils import MISSING

__all__ = ("HTTPClient", "HTTPSession")


async def json_or_text(response: aiohttp.ClientResponse):
    text = await response.text(encoding="utf-8")
    try:
        if "application/json" in response.headers["Content-Type"]:
            return json.loads(text)
    except KeyError:
        pass


class HTTPClient:
    def __init__(self) -> None:
        self.__session: aiohttp.ClientSession = MISSING
        self.token: Optional[str] = None
        user_agent = "Misskey Bot (https://github.com/yupix/MiPA {0}) Python/{1[0]}.{1[1]} aiohttp/{2}"  # noqa: E501
        self.user_agent = user_agent.format(
            __version__, sys.version_info, aiohttp.__version__
        )

    async def close_session(self):
        await self.__session.close()

    async def ws_connect(self, url: str, *, compress: int = 0) -> Any:
        kwargs = {
            "autoclose": False,
            "max_msg_size": 0,
            "timeout": 30.0,
            "headers": {"User-Agent": self.user_agent},
            "compress": compress,
        }
        try:
            ws = await self.__session.ws_connect(url, **kwargs)
        except aiohttp.client_exceptions.ClientConnectorError:
            raise ClientConnectorError()
        return ws


HTTPSession: HTTPClient = HTTPClient()
