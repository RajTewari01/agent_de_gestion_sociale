import importlib.util
from pathlib import Path
from types import ModuleType

base_path : Path = Path(__file__).parents[3].resolve().absolute()
spec = importlib.util.spec_from_file_location("src.backend.plugins.loader",  base_path / "src/backend/plugins/loader.py")

import sys
_plugins_module : ModuleType = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = _plugins_module
spec.loader.exec_module(_plugins_module)

plugins_loader : ModuleType = _plugins_module.PluginLoader().bootstrap()
CONFIG = plugins_loader.config_service.config.CONFIG
BaseAppConfig = plugins_loader.config_service.base.BaseAppConfig

