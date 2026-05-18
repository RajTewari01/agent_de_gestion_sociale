from __future__ import annotations
import sqlite3
from pathlib import Path
from abc import ABC,abstractmethod
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any,TypeAlias,Union,Optional

PathLike : TypeAlias = Union[Path,str]

class BaseDb(ABC):
    def __init__(
        self,
        db_path:PathLike,
        raise_exception:bool=True
        ): 
        self.db_path : PathLike = Path(db_path)
        self.conn:Optional[sqlite3.Connection] = None
        self.raise_exception : bool = raise_exception

    @abstractmethod
    def create(self)->Any:pass
    @abstractmethod
    def read(self)->Any:pass
    @abstractmethod
    def update(self)->Any:pass
    @abstractmethod
    def delete(self)->Any:pass

    def __enter__(self) -> 'BaseDb':
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            else:
                self.conn.rollback()
            self.conn.close()
            self.conn = None
            if self.raise_exception:
                return False # <-raise exception 
            return True # <-supress exception



class DbManager(ABC):
    def __init__(
        self,
        db_path:PathLike,
        raise_exception:bool=True
        ): 
        self.db_path : PathLike = Path(db_path)
        self.raise_exception : bool = raise_exception

    @abstractmethod
    def create(self)->Any:pass
    @abstractmethod
    def read(self)->Any:pass
    @abstractmethod
    def update(self)->Any:pass
    @abstractmethod
    def delete(self)->Any:pass

    @contextmanager
    def get_db_connection(self) -> Generator[sqlite3.Connection, None, None]:
        conn : sqlite3.Connection = sqlite3.connect(self.db_path,check_same_thread=False)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            if self.raise_exception:
                raise RuntimeError(f"Runtime error in DB Manager: {str(e)}") from e
        finally:
            conn.close()

        
 
        

