from abc import ABC

from mipac.models.note import Note


class AbstractTimeline(ABC):
    async def on_note(self, note: Note):
        pass
