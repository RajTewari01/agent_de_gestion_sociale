# ADR - Plugin Manifest System

> Created: 2026-05-17
> Tags: #adr #architecture #plugin-system
> Status: 🟢 Accepted

---

## Context

The project has multiple backend packages (`core`, `config`, `services`) that need to import each other. Running individual files requires either `python -m` flags or `sys.path.insert()` hacks scattered across `__init__.py` files. This doesn't scale as the project grows and makes the codebase fragile.

## Decision

Use XML manifest files to declare each service's modules, and a central `PluginLoader` that uses `importlib.util.spec_from_file_location()` to load modules by file path — completely avoiding `sys.path` manipulation.

## Options Considered

### Option A — sys.path hacks in __init__.py
**Pros:**
- Simple, everyone knows it
- No infrastructure needed

**Cons:**
- Fragile, order-dependent
- Scattered across files
- Breaks IDE type checking
- Doesn't scale

### Option B — Package installation with pip install -e .
**Pros:**
- Standard Python approach
- IDE-friendly

**Cons:**
- Requires virtual env management
- pyproject.toml must list all entry points
- Extra setup step for new devs

### Option C — XML Manifest + importlib.util (chosen)
**Pros:**
- Zero sys.path modification
- Modules lazy-loaded (fast startup)
- Dependency validation before loading
- Easy to add new services (just add XML)
- Self-documenting (XML is human-readable)

**Cons:**
- Custom infrastructure to maintain
- Devs must learn the manifest format
- IDE won't auto-complete through the loader

## Consequences

### Positive
- Any file can be initialized without `-m` or sys hacks
- Adding a new service = one XML file
- Dependencies validated upfront (fast failure)
- Boot order controlled via `<priority>`

### Negative
- IDE autocomplete won't work through `loader.core_service.api_config`
- Custom system means custom bugs
- XML parsing adds slight overhead (mitigated by lazy loading)

## Related
- [[Plugin Architecture]]
- [[Agent de Gestion Sociale]]
