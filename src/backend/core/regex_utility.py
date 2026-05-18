from __future__ import annotations
from typing import List,Pattern,Callable,TypeAlias
from pathlib import Path
import re   
import unicodedata
import emoji # type:ignore

RegStep : TypeAlias = Callable[[str], str]
TruncateStep : TypeAlias = Callable[[str,int,bool],str]

class RegexUtility:
    WHITE_SPACES : Pattern[str] = re.compile(r'\s+')
    HIGH_UNICODE : Pattern[str] = re.compile(r'[\U00010000-\U0010ffff]',flags=re.UNICODE) 

    def __init__(self,text:str):
        self.original : str = text
        self._text : str = text
        self.temp_text: str | None = None
        self.steps : List[RegStep] = []
        self._truncate : RegStep | None = None
    
    def __str__(self)->str:
        return self._text

    def __repr__(self)->str:
        return (
                    f"class name : { self.__class__.__name__}\n"
                    f"stem_name : {Path(__file__).stem}\n"
                    f"filename : {Path(__file__).name}\n"
                    f"file_extension : {Path(__file__).suffix}\n"
                    f"file_path : {Path(__file__)}\n"
                    f"original text : {self.original}\n"
                    f"processed text : {self._text}\n"
                    f"number of steps : {len(self.steps)}\n"
                )
    
    def __len__(self)->int:
        return len(self._text)  

    def __eq__(self, others : 'RegexUtility' | str):
        if isinstance(others,str):
            return self._text == others
        if isinstance(others,RegexUtility):
            return self._text == others._text
        return False
    
    def __hash__(self) -> int:
        return hash(self._text)
        
    def add(self,step:RegStep):
        """
        For adding custom regex steps to the pipeline.
        >>> NOTE : 
            - The steps are executed in the order they are added.
            - The truncate step is executed last.
            - The truncate step is not added to the steps list.
        
        >>> EXAMPLE :
            >>> r = RegexUtility("Hello World")
            >>> r.add(lambda x: x.upper())
            >>> r.build()
            >>> print(r.text)
            HELLO WORLD
        """
        self.steps.append(step)
        return self

    def reset(self):
        self._text = self.original
        self.clear_steps()
        return self
    
    def clear_steps(self):
        self.steps.clear()
        return self

    def build(self):
        result : str = self._text
        for step in self.steps:
            result = step(result)
        if self._truncate is not None:
            result = self._truncate(result)
        self._truncate = None
        self._text = result
        self.clear_steps()
        return self

    @property
    def text(self)->str:
        return self._text

    @text.setter
    def text(self,value:str)->None:
        if not isinstance(value,str): 
            raise TypeError(f"'expected str, got {type(value).__name__}'") 
        if not value:
            raise ValueError("'value cannot be an empty string'")
        self.temp_text = self._text
        self._text = value

    @text.deleter
    def text(self) -> None:
        self._text = self.temp_text if self.temp_text is not None else self._text

    def append_str(self,val:str,spaces:bool=True)->'RegexUtility':
        if not isinstance(val,str): 
            raise TypeError(f"'expected str, got {type(val).__name__}'") 
        if not val:
            raise ValueError("'value cannot be an empty string'")
        if spaces: self.steps.append(lambda x,v=val:x + ' ' + v)
        else: self.steps.append(lambda x,v=val:x + v)
        return self
    
    def prepend_str(self,val:str,spaces:bool=True)->'RegexUtility':
        if not isinstance(val,str): 
            raise TypeError(f"'expected str, got {type(val).__name__}'") 
        if not val:
            raise ValueError("'value cannot be an empty string'")
        if spaces: self.steps.append(lambda x,v=val:v + ' ' + x)
        else: self.steps.append(lambda x,v=val:v + x)
        return self
    
    def use_default(self)->'RegexUtility':
        return self.lower().strip_extra_spaces()
    
    def lower(self)->'RegexUtility':
        self.steps.append(lambda x:x.lower())
        return self
    
    def upper(self)->'RegexUtility':
        self.steps.append(lambda x:x.upper())
        return self
    
    def strip(self)->'RegexUtility':
        self.steps.append(lambda x:x.strip())
        return self
    
    def lstrip(self)->'RegexUtility':
        self.steps.append(lambda x:x.lstrip())
        return self
    
    def rstrip(self)->'RegexUtility':
        self.steps.append(lambda x:x.rstrip())
        return self
    
    def capitalize(self)->'RegexUtility':
        self.steps.append(lambda x:x.capitalize())
        return self
    
    def title(self)->'RegexUtility':
        self.steps.append(lambda x:x.title())
        return self
    
    def swapcase(self)->'RegexUtility':
        self.steps.append(lambda x:x.swapcase())
        return self
    
    def strip_spaces(self)->'RegexUtility':
        self.steps.append(lambda x:self.WHITE_SPACES.sub('',x).strip())
        return self
    
    def strip_extra_spaces(self)->'RegexUtility':
        self.steps.append(lambda x:self.WHITE_SPACES.sub(' ',x))
        return self
    
    def normalize_unicode(self, form='NFC')->'RegexUtility':
        """
        NOTE :
            >>> NFC: Canonical Composition (default, best for most text)
            >>> NFKC: Compatibility Composition (best for search/matching)
        """
        self.steps.append(lambda s,f=form: unicodedata.normalize(f, s))
        return self
    
    def keep_ascii_only(self)->'RegexUtility':
        self.steps.append(lambda s,f='NFKD': unicodedata.normalize(f, s).encode('ascii', 'ignore').decode('utf-8', 'ignore'))
        return self
    
    def strip_high_unicode_chars(self)->'RegexUtility':
        self.steps.append(lambda s: self.HIGH_UNICODE.sub('', s))
        return self

    def strip_emoji(self)->'RegexUtility':
        self.steps.append(lambda s: emoji.replace_emoji(s, replace='')) # type: ignore
        return self
    
    def replace(self,target:str,replace_with:str,count:int=0)->'RegexUtility':
        self.steps.append(lambda current_text,t=target,r=replace_with,c=count: re.sub(t,r,current_text,count=c))
        return self
    
    def truncate(self,max_len:int,from_end:bool=False)->'RegexUtility':
        self.steps.append(lambda x,m=max_len,e=from_end : x[:m] if not e else x[-m:])
        return self

    def truncate_at_last(self,max_len:int,from_end:bool=False)->'RegexUtility':
        self._truncate = lambda x,m=max_len,e=from_end : x[:m] if not e else x[-m:]
        return self

if __name__ == "__main__":

    # ─── BASIC ────────────────────────────────────────────
    print(f"lower          : {RegexUtility('HELLO WORLD').lower().build()}")
    print(f"upper          : {RegexUtility('hello world').upper().build()}")
    print(f"capitalize     : {RegexUtility('hello world').capitalize().build()}")
    print(f"title          : {RegexUtility('hello world').title().build()}")
    print(f"swapcase       : {RegexUtility('Hello World').swapcase().build()}")

    # ─── STRIP ────────────────────────────────────────────
    print(f"strip          : {RegexUtility('  hello world  ').strip().build()}")
    print(f"lstrip         : {RegexUtility('  hello world  ').lstrip().build()}")
    print(f"rstrip         : {RegexUtility('  hello world  ').rstrip().build()}")
    print(f"strip_extra    : {RegexUtility('hello   world').strip_extra_spaces().build()}")
    print(f"strip_spaces   : {RegexUtility('hello   world').strip_spaces().build()}")

    # ─── DEFAULT ──────────────────────────────────────────
    print(f"use_default    : {RegexUtility('HELLO   WORLD  ').use_default().build()}")

    # ─── APPEND / PREPEND ─────────────────────────────────
    print(f"append(space)  : {RegexUtility('hello').append_str('world').build()}")
    print(f"append(no sp)  : {RegexUtility('hello').append_str('world', spaces=False).build()}")
    print(f"prepend(space) : {RegexUtility('world').prepend_str('hello').build()}")
    print(f"prepend(no sp) : {RegexUtility('world').prepend_str('hello', spaces=False).build()}")

    # ─── UNICODE ──────────────────────────────────────────
    print(f"norm NFC       : {RegexUtility('café').normalize_unicode(form='NFC').build()}")
    print(f"norm NFKC      : {RegexUtility('café').normalize_unicode(form='NFKC').build()}")
    print(f"ascii only     : {RegexUtility('café').keep_ascii_only().build()}")
    print(f"strip high uni : {RegexUtility('hello 𠀋 world').strip_high_unicode_chars().build()}")

    # ─── EMOJI ────────────────────────────────────────────
    print(f"strip emoji    : {RegexUtility('hello 😊🔥 world').strip_emoji().build()}")

    # ─── REPLACE ──────────────────────────────────────────
    print(f"replace all    : {RegexUtility('aaa bbb aaa').replace('aaa', 'ccc').build()}")
    print(f"replace count=1: {RegexUtility('aaa bbb aaa').replace('aaa', 'ccc', count=1).build()}")

    # ─── TRUNCATE ─────────────────────────────────────────
    print(f"truncate front : {RegexUtility('hello world').truncate(5).build()}")
    print(f"truncate end   : {RegexUtility('hello world').truncate(5, from_end=True).build()}")
    print(f"trunc_last frt : {RegexUtility('hello world').truncate_at_last(5).build()}")
    print(f"trunc_last end : {RegexUtility('hello world').truncate_at_last(5, from_end=True).build()}")

    # ─── PROPERTY ─────────────────────────────────────────
    ru = RegexUtility("hello world").lower().build()
    print(f"getter         : {ru.text}")
    ru.text = "RAJ TEWARI"
    print(f"setter         : {ru.text}")
    del ru.text
    print(f"deleter        : {ru.text}")

    # ─── CHAINING ─────────────────────────────────────────
    print(f"chaining       : {RegexUtility('  HELLO 😊 WORLD 𠀋  ').lower().strip().strip_emoji().strip_high_unicode_chars().strip_extra_spaces().build()}")

    # ─── DUNDER ───────────────────────────────────────────
    ru1 = RegexUtility("HELLO").lower().build()
    ru2 = RegexUtility("hello").build()
    print(f"eq (ru==ru)    : {ru1 == ru2}")
    print(f"eq (ru==str)   : {ru1 == 'hello'}")
    print(f"len            : {len(ru1)}")
    print(f"repr           :\n{repr(ru1)}")
    print(f"str            : {str(ru1)}")

    # ─── HASH ─────────────────────────────────────────────
    seen = set()
    seen.add(RegexUtility("HELLO").lower().build())
    seen.add(RegexUtility("hello").build())
    print(f"hash dedup     : {len(seen)}")

    # ─── RESET ────────────────────────────────────────────
    ru = RegexUtility("HELLO WORLD").lower().build()
    print(f"before reset   : {ru}")
    ru.reset()
    print(f"after reset    : {ru}")

    # ─── CUSTOM STEP ──────────────────────────────────────
    ru = RegexUtility("hello world").add(lambda x: x.replace("world", "RAJ")).build()
    print(f"custom add     : {ru}")