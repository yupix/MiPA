from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Iterable, Literal, overload


if TYPE_CHECKING:
    from mipa.ext.timelines.core import AbstractTimeline
    from aiohttp.client_ws import ClientWebSocketResponse

__all__ = ["Router"]

IChannel = Literal["global", "main", "home", "local", "hybrid"]


CHANNELS = {
    "global": "globalTimeline",
    "main": "main",
    "home": "homeTimeline",
    "local": "localTimeline",
    "hybrid": "hybridTimeline",
}


class Router:
    def __init__(
        self, web_socket: ClientWebSocketResponse, max_capure: int = 100
    ):
        self.web_socket: ClientWebSocketResponse = web_socket
        self.captured_note: list[str] = []
        self.max_capture: int = max_capure
        self.__channel_ids: dict[str, IChannel] = {}
        self.__channel_handlers: dict[str, AbstractTimeline] = {}

    @overload
    async def connect_channel(self, channel_list: Iterable[IChannel]):
        ...

    @overload
    async def connect_channel(
        self, channel_list: dict[IChannel, AbstractTimeline | None]
    ):
        ...

    async def connect_channel(
        self,
        channel_list: Iterable[IChannel]
        | dict[IChannel, AbstractTimeline | None],
    ):
        """
        Connects to a channel based on the list passed.

        Parameters
        ----------
        channel_list : IChannel
            ['global', 'main', 'home', 'local', 'hybrid']

        Returns
        -------
        dict[IChannel, str]
        """

        _channel_ids: dict[IChannel, str] = {}
        try:
            for channel in channel_list:
                channel_id = f"{uuid.uuid4()}"
                _channel_ids[channel] = channel_id
                self.__channel_ids[channel_id] = channel
                if isinstance(channel_list, dict):
                    channel_handler = channel_list[channel]
                    if channel_handler:
                        self.__channel_handlers[channel_id] = channel_handler

                await self.web_socket.send_json(
                    {
                        "type": "connect",
                        "body": {
                            "channel": f"{CHANNELS[channel]}",
                            "id": f"{_channel_ids[channel]}",
                        },
                    }
                )
        except KeyError:
            pass
        return _channel_ids

    async def disconnect_channel(self, channel_id: str):
        """
        Disconnects from a channel based on the id passed.

        Parameters
        ----------
        channel_id : str
        """

        self.__channel_ids.pop(channel_id)
        await self.web_socket.send_json(
            {"type": "disconnect", "body": {"id": f"{channel_id}"}}
        )

    async def capture_message(self, note_id: str) -> None:
        """
        Captures a message based on the id passed.
        Parameters
        ----------
        note_id : str
        """
        if len(self.captured_note) > self.max_capture:
            await self.web_socket.send_json(
                {"type": "unsubNote", "body": {"id": f"{note_id}"}}
            )
            del self.captured_note[0]
        self.captured_note.append(note_id)
        await self.web_socket.send_json(
            {"type": "subNote", "body": {"id": f"{note_id}"}}
        )

    @property
    def channel_ids(self) -> dict[str, IChannel]:
        """
        Returns the unique ID of the connected channel and the channel mapping

        Returns
        -------
        dict[str, IChannel]
        """
        return self.__channel_ids

    @property
    def channel_handlers(self) -> dict[str, AbstractTimeline]:
        """
        Returns the unique ID of the connected channel and the channel mapping

        Returns
        -------
        dict[str, AbstractTimeline]
        """
        return self.__channel_handlers
