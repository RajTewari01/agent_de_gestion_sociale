from pathlib import Path
from typing import TypeAlias,Callable,Optional,Union
from functools import wraps
from sys import exc_info
from .paths import DEBUG
import traceback

PathLike : TypeAlias = Union[Path,str]

class CaptureException(RuntimeError):
    pass

def capture_exceptions(
                        func:Callable=None, 
                        max_attempts:Optional[int]=None, 
                        raise_exception: bool = DEBUG, 
                        log_exception: bool = False,
                        file_path:Optional[PathLike]=None
                        ):
    def decorator(function:Callable):
        @wraps(function)
        def wrapper(*args, **kwargs):
            attempts : int = max_attempts or 1
            for i in range(1, attempts+1):
                try:
                    return function(*args,**kwargs)
                except Exception :
                    exc_type, exc_value, exc_tb = exc_info()
                    last = traceback.extract_tb(exc_tb)[-1]

                    error_data = {
                        "func_name": function.__name__,
                        "func_path": function.__code__.co_filename,
                        "error_type": exc_type.__name__,
                        "error_value": str(exc_value),
                        "error_file": last.filename,
                        "error_func": last.name,
                        "error_line": last.lineno,
                        "attempt": i
                        }

                    if i >= attempts and raise_exception:  
                        raise CaptureException(error_data) from exc_value

        return wrapper

    if func is not None and callable(func):
        return decorator(function=func)
    return decorator

            