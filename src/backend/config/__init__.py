from typing import List
from pathlib import Path
import importlib.util
from types import ModuleType

base_path : Path = Path(__file__).parents[3].resolve().absolute() 
spec = importlib.util.spec_from_file_location("src.backend.plugins.loader",  base_path / "src/backend/plugins/loader.py")

import sys
_plugins_module : ModuleType = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = _plugins_module
spec.loader.exec_module(_plugins_module)

plugins_loader : ModuleType = _plugins_module.PluginLoader().bootstrap()
get_config = plugins_loader.config_service.loader.get_config
BaseAppConfig = plugins_loader.config_service.base.BaseAppConfig


CONFIG : BaseAppConfig = get_config()
__all__ : List = ["CONFIG", "plugins_loader", "get_config", "BaseAppConfig", "DevConfig", "ProdConfig"]