from __future__ import annotations
from pathlib import Path
from sys import path
from typing import (
    TypeAlias,List,Union
)
import pydantic as pdt  #type: ignore
from . import CONFIG, BaseAppConfig

DEBUG : bool = CONFIG.DEBUG
BASE : Path = Path(__file__).parents[3].resolve().absolute()


PathLike : TypeAlias = Union[Path,str]

DIRECTORY_LIST : List = ['assets','src/backend/config','data/db','data/downloaded/music','data/downloaded/song','data/downloaded/video','data/downloaded/image','deploy/docker','deploy/k8s','deploy/terraform','docs','env','tests']

class Paths(pdt.BaseModel,strict=True, extra="forbid"):

    root : Path = pdt.Field(default_factory=lambda:BASE)
    debug : bool = pdt.Field(default_factory=lambda:DEBUG)
    app_config : BaseAppConfig = pdt.Field(default_factory=lambda:CONFIG)
    ensure : bool = True
    

    @property
    def docker_path(self) -> Path:
        return self.root / "deploy/docker"

    @property
    def k8s_path(self) -> Path:
        return self.root / "deploy/k8s"
    
    @property
    def terraform_path(self) -> Path:
        return self.root / "deploy/terraform"
    
    @property
    def docs_path(self) -> Path:
        return self.root / "docs"
    
    @property
    def env_path(self) -> Path:
        return self.root / "env"
    
    @property
    def assets_path(self) -> Path:
        return self.root / "assets"
    
    @property
    def config_path(self) -> Path:
        return self.root / "src/backend/config"
    
    @property
    def data_path(self) -> Path:
        return self.root / "data"
    
    @property
    def downloaded_path(self) -> Path:
        return self.root / "data/downloaded"
    
    @property
    def db_path(self) -> Path:
        return self.root / "data/db"
    
    @property
    def music_path(self) -> Path:
        return self.root / "data/downloaded/music"
    
    @property
    def song_path(self) -> Path:
        return self.root / "data/downloaded/song"
    
    @property
    def video_path(self) -> Path:
        return self.root / "data/downloaded/video"
    
    @property
    def image_path(self) -> Path:
        return self.root / "data/downloaded/image"
    
    @property
    def logs_path(self) -> Path:
        return self.root / "data/logs"
    
    @property
    def src(self) -> Path:
        return self.root / "src"
    
    @property
    def backend(self) -> Path:
        return self.root / "src/backend"
    
    @property
    def frontend(self) -> Path:
        return self.root / "src/frontend"
    
    @property
    def tests(self) -> Path:
        return self.root / "tests"

    def __init__(self,**data):
        super().__init__(**data)
        if self.ensure:
            FileManager().ensure_all(*(self.root/dir_name for dir_name in DIRECTORY_LIST))

class FileManager:
    """
    File manager for creating and managing files and directories.
    """
    def ensure_dir(self,*names:PathLike)->'FileManager':
        for name in map(Path,names):
            name.mkdir(parents=True,exist_ok=True)
        return self
    
    def ensure_file(self,*names:PathLike)->'FileManager':
        for name in map(Path,names):
            name.touch(exist_ok=True)
        return self
    
    def create_symlink(self,source:str,link:PathLike)->Path:
        Path(link).symlink_to(source)
        return Path(link)
    
    def ensure_all(self,*names:PathLike)->None:
        for name in map(Path,names):
            if name.suffix:
                self.ensure_file(name)
            self.ensure_dir(name)
        return 
    
    def __repr__(self) -> str:
        return  (
                    f"class name : { self.__class__.__name__}\n"
                    f"stem_name : {Path(__file__).stem}\n"
                    f"filename : {Path(__file__).name}\n"
                    f"file_extension : {Path(__file__).suffix}\n"
                    f"file_path : {Path(__file__)}\n"
                )

if __name__ == '__main__':
    print(FileManager().__doc__)
    print(CONFIG)
    print(DEBUG)