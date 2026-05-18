# Plugin Architecture — Agent de Gestion Sociale

## Overview

The plugin system replaces `sys.path` hacks and `python -m` flags with a clean, manifest-driven module loader. Each service declares its modules in an XML file, and the `PluginLoader` reads those manifests to make modules importable from anywhere — using **only `importlib.util`**, never touching `sys.path`.

---

## Directory Structure

```
src/backend/plugins/
├── loader.py                    ← The PluginLoader engine
└── manifest/
    ├── CoreService.xml          ← Manifest for src/backend/core
    ├── ConfigService.xml        ← (future) Manifest for src/backend/config
    └── ...                      ← One XML per service
```

---

## How It Works (Step by Step)

### 1. You Write an XML Manifest

Each service gets one XML file declaring what modules it exposes:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest version="1.0">
    <plugin id="core_service">
        <metadata>
            <name>CoreService</name>
            <version>1.0.0</version>
            <author>Raj</author>
        </metadata>
        <runtime>
            <enabled>true</enabled>
            <priority>1</priority>      <!-- lower = loads first -->
        </runtime>
        <modules>
            <module name="paths">src.backend.core.paths</module>
            <module name="api_config">src.backend.core.api_config</module>
            <module name="capture_exceptions">src.backend.core.capture_exceptions</module>
        </modules>
        <dependencies>
            <package version=">=2.0.0">pydantic</package>
        </dependencies>
    </plugin>
</manifest>
```

The `name` attribute is the **alias** you'll use in Python. The text is the **dotted module path**.

### 2. The Loader Reads All Manifests

```python
from src.backend.plugins.loader import PluginLoader

loader = PluginLoader().bootstrap()
```

`bootstrap()` does three things in order:

```
discover()  →  validate()  →  register namespaces
     │              │               │
     │              │               └─ Creates a PluginNamespace per plugin
     │              │                  (modules are NOT imported yet)
     │              │
     │              └─ Checks all <package> deps are pip-installed
     │                 e.g. can we find "pydantic" via importlib.util.find_spec?
     │
     └─ Scans manifest/*.xml, parses each into a PluginManifest dataclass
        Skips any with <enabled>false</enabled>
```

### 3. You Access Modules — They Load Lazily

```python
# Nothing is imported until you touch it
loader.core_service.api_config    # ← imports NOW, first access
loader.core_service.api_config    # ← cached, instant
```

This is powered by `__getattr__` on `PluginNamespace`. Only when you access `.api_config` does it actually load the file.

---

## How Modules Load (No sys.path)

The traditional way requires `sys.path` manipulation:

```python
# ❌ The old way
import sys
sys.path.insert(0, "d:/agent_de_gestion_sociale")
from src.backend.core.api_config import fetch_apikey
```

The plugin loader uses `importlib.util` to load by **file path** directly:

```python
# What the loader does internally
import importlib.util

spec = importlib.util.spec_from_file_location(
    "src.backend.core.api_config",                            # module name
    "d:/agent_de_gestion_sociale/src/backend/core/api_config.py"  # file path
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)   # ← executes the .py file
```

No `sys.path` is ever modified. The file is located directly using the project ROOT.

---

## Key Functions Explained

### `_dotted_to_filepath(dotted_path)`

Converts a dotted Python path to an actual file on disk:

```
"src.backend.core.paths"
         │
         ▼  split(".")
["src", "backend", "core", "paths"]
         │
         ▼  Path(*parts)          ← unpacks list as separate arguments
Path("src/backend/core/paths")
         │
         ▼  .with_suffix(".py")
Path("src/backend/core/paths.py")
         │
         ▼  ROOT / ...
Path("d:/agent_de_gestion_sociale/src/backend/core/paths.py")
```

#### Why `*parts`?

`Path()` accepts each directory level as a separate argument:

```python
parts = ["src", "backend", "core", "paths"]

Path(*parts)        # ✅ Path("src/backend/core/paths")
Path(parts)         # ❌ TypeError — can't pass a list directly
```

The `*` operator **unpacks** the list into individual arguments. It's equivalent to writing `Path("src", "backend", "core", "paths")`.

If the `.py` file doesn't exist, it tries `__init__.py` (for packages):

```
src/backend/core/paths.py       ← try this first
src/backend/core/paths/__init__.py  ← fallback for packages
```

### `_bool(value)`

XML has no native boolean type — everything is a string. This function normalizes XML text to Python booleans:

```python
def _bool(value: str) -> bool:
    return value.lower() in ("true", "1", "yes")
```

```
"true"  → True       "false" → False
"True"  → True       "FALSE" → False
"1"     → True       "0"     → False
"yes"   → True       "no"    → False
```

This handles the common conventions people use in XML/YAML config files, so `<enabled>true</enabled>`, `<enabled>True</enabled>`, and `<enabled>1</enabled>` all work.

### `_text(element)`

Safely extracts text from an XML element without crashing on `None`:

```python
_text(some_element)         # "hello" (stripped)
_text(None)                 # "" (safe default)
_text(None, "fallback")     # "fallback"
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                     CoreService.xml                      │
│                                                          │
│  <module name="paths">src.backend.core.paths</module>    │
│  <module name="api_config">src.backend.core.api_config   │
└──────────────────────┬──────────────────────────────────┘
                       │ parse_manifest()
                       ▼
              ┌─────────────────┐
              │  PluginManifest  │
              │                  │
              │  id: core_service│
              │  modules: {      │
              │    paths → ...   │
              │    api_config →  │
              │  }               │
              └────────┬─────────┘
                       │ bootstrap()
                       ▼
              ┌──────────────────┐
              │  PluginNamespace  │
              │                   │
              │  .__getattr__()   │──── lazy import on first access
              │  ._cache          │──── stores loaded modules
              └────────┬──────────┘
                       │
                       ▼
              ┌──────────────────┐
              │   PluginLoader    │
              │                   │
              │  .core_service    │──→ PluginNamespace
              │  .some_service    │──→ PluginNamespace (future)
              └───────────────────┘
```

---

## Usage Examples

### Basic Usage

```python
from src.backend.plugins.loader import PluginLoader

loader = PluginLoader().bootstrap()

# Access modules through the loader
Paths = loader.core_service.paths.Paths
key   = loader.core_service.api_config.fetch_apikey("pixels_api_key")
```

### Adding a New Service

1. Create your Python modules (e.g., `src/backend/services/scraper.py`)
2. Create `manifest/ScraperService.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<manifest version="1.0">
    <plugin id="scraper_service">
        <metadata>
            <name>ScraperService</name>
            <version>1.0.0</version>
            <author>Raj</author>
        </metadata>
        <runtime>
            <enabled>true</enabled>
            <priority>10</priority>
        </runtime>
        <modules>
            <module name="scraper">src.backend.services.scraper</module>
        </modules>
        <dependencies>
            <package version=">=2.11.0">scrapy</package>
        </dependencies>
    </plugin>
</manifest>
```

3. Use it:

```python
loader = PluginLoader().bootstrap()
loader.scraper_service.scraper.run()
```

### Checking What's Loaded

```python
loader = PluginLoader().bootstrap()

print(loader)
# PluginLoader(plugins=['core_service', 'scraper_service'])

print(loader.core_service)
# PluginNamespace(core_service, loaded=[], available=['paths', 'api_config', 'capture_exceptions'])

# After accessing a module:
_ = loader.core_service.paths
print(loader.core_service)
# PluginNamespace(core_service, loaded=['paths'], available=['paths', 'api_config', 'capture_exceptions'])
```

---

## Priority System

Plugins are registered in priority order (lower number = first):

| Priority | Plugin | Purpose |
|----------|--------|---------|
| 1 | `core_service` | Paths, API config, exception handling |
| 5 | `config_service` | App configuration (future) |
| 10 | `scraper_service` | Web scraping (future) |
| 20 | `media_service` | Video/audio processing (future) |

This matters when plugins depend on each other — lower priority plugins are available first.

---

## Dependency Validation

The loader checks that all `<package>` entries are installed **before** any module is loaded:

```
bootstrap()
    │
    ├─ discover()     ← parse all XMLs
    ├─ validate()     ← check importlib.util.find_spec("pydantic") exists
    │                    check importlib.util.find_spec("pydantic_settings") exists
    │                    ⚠️ raises PluginError if any are missing
    │
    └─ register()     ← create PluginNamespaces (no imports yet)
```

Package names with hyphens are auto-normalized:

```
pydantic-settings  →  pydantic_settings  (for find_spec lookup)
```
