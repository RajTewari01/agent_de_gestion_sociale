# d:/agent_de_gestion_sociale/run.py
# pyrefly: ignore [missing-import]
from src.backend.core.paths import Paths, FileManager 

if __name__ == '__main__':
    print(FileManager().__doc__)
    print(Paths().__repr__())
    print(Paths().app_config.PRODUCTION_VARIABLE)
