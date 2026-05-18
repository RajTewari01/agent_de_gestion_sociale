# Dependencies Tracker

> Tags: #reference #dependencies
> Project: [[Agent de Gestion Sociale]]

---

## Python Packages

| Package | Version | Used By | Purpose |
|---|---|---|---|
| pydantic | >=2.0.0 | core/paths, core/api_config, config/base | Data models, validation |
| pydantic-settings | >=2.0.0 | core/api_config | .env file loading |
| PyYAML | * | config/loader | YAML config parsing |

## Stdlib Modules Used

| Module | Used By | Purpose |
|---|---|---|
| `pathlib` | everywhere | Path management |
| `importlib.util` | core/__init__, plugins/loader | Dynamic module loading |
| `xml.etree.ElementTree` | plugins/loader | XML manifest parsing |
| `dataclasses` | plugins/loader | Plugin data structures |
| `functools` | core/api_config, core/capture_exceptions | caching, wraps |
| `sqlite3` | db/base | Database |
| `traceback` | core/capture_exceptions | Error details |
| `enum` | config/base | ProductionVariable |
| `abc` | db/base | Abstract base classes |
| `contextlib` | db/base | Context managers |

## Future (Not Yet Added)
| Package | For |
|---|---|
| scrapy | Web scraping service |
| fastapi | API layer |
| uvicorn | ASGI server |
| httpx | Async HTTP client |
