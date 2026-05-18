from pydantic_settings import BaseSettings # type:ignore 
from pydantic_settings import SettingsConfigDict # type:ignore 
from pydantic import SecretStr # type:ignore 
from functools import lru_cache,cache
from pathlib import Path
from .paths import DEBUG

ROOT : Path = Path(__file__).resolve().absolute().parents[3]

class ApiConfig(BaseSettings):
    
    pixels_api_key : SecretStr
    pixabay_api_key : SecretStr
    unsplash_api_key : SecretStr

    model_config = SettingsConfigDict(
        env_file = ROOT/"env/secret.env.local",
        env_file_encoding = 'utf-8',
        extra = 'allow'
    )

    def fetch(self, key:str, debug:bool=DEBUG) -> SecretStr:
        if hasattr(self, key): #checks for the attribute in self
            attr = getattr(self,key) 
            if isinstance(attr,SecretStr): #checks if the attribute is an instance of SecretStr
                return attr #returns the attribute

        val : str = self.model_extra.get(key) #gets the attribute from the model_extra
        if not val and debug:
            raise KeyError(f"{key} not found")
        if not val and not debug:
            return SecretStr("")
        return SecretStr(val)

@cache
def api_factory() -> ApiConfig:
    return ApiConfig()

@lru_cache(maxsize=1) 
def fetch_apikey(key:str, debug:bool=DEBUG) -> SecretStr:
    api = ApiConfig()
    return api.fetch(key,debug)

def set_api_key(comment:str = None,**kwargs)->None:
    with open(ROOT/"env/secret.env.local", 'a', encoding='utf-8') as file:
        if comment:
            file.write(f"#{'='*20}\n{comment.lower().title()}\n{'='*20}\n")
        for key, value in kwargs.items():
            file.write(f"{key}={value}\n")

if __name__ == '__main__':
    print(fetch_apikey("pixels_api_key").get_secret_value())
            
        
        
