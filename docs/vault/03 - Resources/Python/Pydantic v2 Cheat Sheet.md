# Pydantic v2 Cheat Sheet

> Tags: #reference #python #pydantic
> Confidence: 🟡 Intermediate

---

## BaseModel Basics

```python
import pydantic as pdt

class User(pdt.BaseModel, strict=True, extra="forbid"):
    name: str
    age: int = pdt.Field(default=0, ge=0)
```

### `strict=True`
- **No type coercion.** If a field expects `int`, passing `"42"` (string) raises `ValidationError`
- Enums must receive the enum member, NOT `.value`:
  ```python
  # ✅ Correct
  PRODUCTION_VARIABLE: MyEnum = MyEnum.PRODUCTION
  
  # ❌ Breaks with strict=True
  PRODUCTION_VARIABLE: MyEnum = MyEnum.PRODUCTION.value
  ```

### `extra="forbid"`
- Passing unknown fields raises an error
- Use `extra="allow"` to accept arbitrary fields (stored in `model_extra`)

## SecretStr

```python
from pydantic import SecretStr

class Config(pdt.BaseModel):
    api_key: SecretStr

c = Config(api_key="sk-123")
print(c.api_key)                    # SecretStr('**********')
print(c.api_key.get_secret_value()) # sk-123
```

## pydantic-settings

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class ApiConfig(BaseSettings):
    api_key: SecretStr

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"
    )
```

Reads from `.env` file automatically. Field names match env var names (case-insensitive).

## Common Gotchas

> [!WARNING] 
> `model_extra` is `None` if `extra="forbid"` (default). Only populated with `extra="allow"`.

> [!WARNING]
> `default_factory` must be a callable, not a value:
> ```python
> # ✅
> root: Path = pdt.Field(default_factory=lambda: Path("."))
> # ❌
> root: Path = pdt.Field(default_factory=Path("."))
> ```

## Related
- [[Module - API Config]]
- [[Module - Paths]]
- [[ADR - Pydantic Strict Mode]]
