from .base import BaseAppConfig
from .dev import DevConfig
from .prod import ProdConfig
import yaml
from pathlib import Path

ROOT : Path = Path(__file__).parents[3]
APP_ENV : Path = ROOT / "config/app_config.yaml"

def get_config() -> BaseAppConfig:
    try:
        with open(APP_ENV, 'r', encoding='utf-8') as file:
            env = yaml.safe_load(file)
    except Exception as e:
        raise RuntimeError(str(e)) from e
    stage : str = env.get("app", {}).get("stage", "development")
    match stage:
        case "production":
            return ProdConfig()
        case "development":
            return DevConfig()
        case _:
            return DevConfig()
        
    
if __name__ == "__main__":
    print(get_config())

    
