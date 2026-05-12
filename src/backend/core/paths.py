from __future__ import annotations
from pathlib import Path
from sys import path
from typing import (
    TypeAlias,Callable,List,Tuple,Dict,Any,Optional,Iterable
)

BASE : Path = Path(__file__).parents[3]

ReprType : TypeAlias = Tuple[Dict[str,Any]]

class Paths:
    __slots__ = []
    def __init__(self):pass
    def __repr__(self) -> str:
        return (
            {
                'class' : self.__class__.__name__,
                'file'  : __file__,
            }
        )
    def __str__(self) -> str: pass
    def __eq__(self,other: Any) -> bool: 
        if isinstance(other,Paths):
            pass

class FileManager:
    def ensure_dir(self,*names)->None:
        for name in map(Path,names):
            name.mkdir(parents=True,exist_ok=True)
    
    def ensure_file(self,*names)->None:
        for name in map(Path,names):
            name.touch(exist_ok=True)
    
    def create_symlink(self,source:str,link:str)->Path:
        Path(link).symlink_to(source)
        return Path(link)
    
    def ensure_all(self,names:Iterable[Path])->None:
        try:
            for name in names: self.ensure_dir(name) if name.is_dir() else self.ensure_file(name)
        except Exception as e:
            pass
             
        
            
            

    


            
            

print(Paths().__repr__())