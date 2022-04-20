from mipac.http import HTTPClient
from mipac.manager.client import ClientActions


class Client:
    def __init__(self, url: str, token: str):
        self.__url: str = url
        self.__token: str = token
        self.session: HTTPClient = HTTPClient(url, token)

    @property
    def action(self):
        return ClientActions(self.session)

    async def close_session(self):
        await self.session.close_session()
