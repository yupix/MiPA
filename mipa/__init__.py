__title__ = 'mipa'
__author__ = 'yupix'
__license__ = 'MIT'
__copyright__ = 'Copyright 2022-present yupix'
__author_email__ = 'yupi0982@outlook.jp'
__version__ = '0.0.3a'

__path__ = __import__('pkgutil').extend_path(__path__, __name__)

from .client import Client
from .ext import *

__all__ = ('Client',)
