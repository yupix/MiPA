from typing import Optional

__all__ = ['RawInstance']

from mipac.types import InstancePayload


class RawInstance:
    """
    Attributes
    ----------
    host : Optional[str], default=None
    name : Optional[str], default=None
    software_name : Optional[str], default=None
    software_version : Optional[str], default=None
    icon_url : Optional[str], default=None
    favicon_url : Optional[str], default=None
    theme_color : Optional[str], default=None
    """

    __slots__ = ('host', 'name', 'software_name', 'software_version', 'icon_url', 'favicon_url', 'theme_color')

    def __init__(self, data: InstancePayload):
        self.host: Optional[str] = data.get('host')
        self.name: Optional[str] = data.get('name')
        self.software_name: Optional[str] = data.get('software_version')
        self.software_version: Optional[str] = data.get('software_version')
        self.icon_url: Optional[str] = data.get('icon_url')
        self.favicon_url: Optional[str] = data.get('favicon_url')
        self.theme_color: Optional[str] = data.get('theme_color')
