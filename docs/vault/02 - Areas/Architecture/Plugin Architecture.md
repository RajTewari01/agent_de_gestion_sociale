# Plugin Architecture

> Tags: #architecture #plugin-system #reference
> Source: `d:\agent_de_gestion_sociale\docs\plugin_architecture.md`

---

## What Is It?

A manifest-driven module loader that replaces `sys.path` hacks and `python -m` flags. Each service declares its modules in an XML file, and the `PluginLoader` makes them importable from anywhere using pure `importlib.util`.

## How It Works

```
XML Manifest  →  PluginLoader.bootstrap()  →  PluginNamespace  →  lazy import
```

1. **XML declares modules** — each `<module name="alias">dotted.path</module>`
2. **Loader discovers & validates** — scans `manifest/*.xml`, checks pip deps
3. **Namespace exposes modules** — `loader.core_service.api_config` triggers import on first access
4. **importlib.util loads by file path** — dotted path → file path → `spec_from_file_location`

## Key Insight

```python
# ❌ Old way (sys.path hack)
import sys
sys.path.insert(0, "d:/agent_de_gestion_sociale")
from src.backend.core.api_config import fetch_apikey

# ✅ New way (plugin loader)
loader = PluginLoader().bootstrap()
loader.core_service.api_config.fetch_apikey("pixels_api_key")
```

## Files
- `src/backend/plugins/loader.py` — the loader engine
- `src/backend/plugins/manifest/*.xml` — service manifests
- `docs/plugin_architecture.md` — full technical docs

## Related
- [[Agent de Gestion Sociale]]
- [[Module - Plugin Loader]]
- [[ADR - Plugin Manifest System]]
