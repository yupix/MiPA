from ._version import get_versions

__title__ = "mipa"
__author__ = "yupix"
__license__ = "MIT"
__copyright__ = "Copyright 2022-present yupix"
__author_email__ = "yupi0982@outlook.jp"
__version__ = get_versions()["version"]

__path__ = __import__("pkgutil").extend_path(__path__, __name__)

del get_versions

from .client import Client
from .ext import *

__all__ = ("Client",)

from . import _version

__version__ = _version.get_versions()["version"]
