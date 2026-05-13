from __future__ import annotations
from pathlib import Path
from sys import path
from typing import (
    TypeAlias,Callable,List,Tuple,Dict,Any,Optional,Iterable,Union
)
import pydantic as pdt  #type: ignore

BASE : Path = Path(__file__).parents[3]


ReprType : TypeAlias = Tuple[Dict[str,Any]]

DIRECTORY_LIST : List = ['assets','src/backend/config','data/db','data/downloaded/music','data/downloaded/song','data/downloaded/videos','data/downloaded/images','deploy/docker','deploy/k8s','deploy/terraform','docs','env','test']

class Paths(pdt.BaseModel,strict=True, extra="forbid"):

    def __init__(self,ensure:bool=True,**data):
        super().__init__(**data)
        self.ensure = ensure
        if self.ensure:
            self.ensure_all(*(self.root/dir_name for dir_name in DIRECTORY_LIST))

class FileManager:
    """
    File manager for creating and managing files and directories.
    """
    def ensure_dir(self,*names)->None:
        for name in map(Path,names):
            name.mkdir(parents=True,exist_ok=True)
    
    def ensure_file(self,*names)->None:
        for name in map(Path,names):
            name.touch(exist_ok=True)
    
    def create_symlink(self,source:str,link:Union[str|Path])->Path:
        Path(link).symlink_to(source)
        return Path(link)
    
    def ensure_all(self,names:Iterable[Union[Path|str]])->None:
        for name in map(Path,names):
            if name.suffix:
                self.ensure_file(name)
            else:
                self.ensure_dir(name)
    
    def repr(self) -> str:
        return  (
                    f"class name : { self.__class__.__name__}\n"
                    f"stem_name : {Path(__file__).stem}\n"
                    f"filename : {Path(__file__).name}\n"
                    f"file_extension : {Path(__file__).suffix}\n"
                    f"file_path : {Path(__file__)}\n"
                )

if __name__ == '__main__':
    print(FileManager().__doc__)
        
            
            

    


            
            

print(Paths().__repr__())