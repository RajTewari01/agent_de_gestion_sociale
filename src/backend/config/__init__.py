from .loader import get_config
from .base import BaseAppConfig
from typing import List

CONFIG : BaseAppConfig = get_config()
__all__ : List = ["CONFIG"]