# Agent de Gestion Sociale

> Created: 2026-05-17
> Tags: #project #active #python
> Repo: `D:\agent_de_gestion_sociale`

---

## Overview

Open-source social automation agent built in Python, designed to run on both local machines and cloud environments. Provides free, accessible tools for social media automation — content creation, scheduling, and distribution.

## Goals
- [ ] Plugin-based architecture with XML manifests
- [ ] Multi-platform social media connectors (Instagram, YouTube, Twitter, Reddit)
- [ ] Media production pipeline (TTS, subtitles, video assembly, thumbnails)
- [ ] Web scraping service
- [ ] Local + cloud deployment support

## Architecture

```
agent_de_gestion_sociale/
├── src/backend/
│   ├── core/           → paths, api_config, capture_exceptions
│   ├── config/         → base, dev, prod, loader (YAML-driven)
│   ├── plugins/        → manifest-driven module loader
│   └── services/       → (empty — future services)
├── config/             → app_config.yaml
├── db/                 → SQLite base classes
├── deploy/             → docker, k8s, terraform
├── env/                → secret.env.local
└── main.py             → entry point
```

### Key Architecture Decisions
- [[ADR - Plugin Manifest System]] — XML manifests + importlib loader
- [[ADR - Pydantic Strict Mode]] — strict=True on all models

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Config Models | Pydantic v2 (strict mode) |
| API Key Mgmt | pydantic-settings |
| Config Format | YAML (PyYAML) |
| Database | SQLite3 (stdlib) |
| Plugin System | Custom XML manifests + importlib.util |
| Infra | Docker, K8s, Terraform |

## Key Modules
- [[Module - Paths]] — directory structure management, FileManager
- [[Module - API Config]] — API key loading via pydantic-settings
- [[Module - Capture Exceptions]] — retry decorator with error capture
- [[Module - Config Loader]] — YAML-based dev/prod config switching
- [[Module - Plugin Loader]] — XML manifest parser + lazy module loader

## Dependencies

| Package | Version | Used By |
|---|---|---|
| pydantic | >=2.0.0 | core/paths, core/api_config, config/base |
| pydantic-settings | >=2.0.0 | core/api_config |
| PyYAML | * | config/loader |

## Known Issues
- [ ] `PRODUCTION_VARIABLE` field is defined but never used for logic
- [ ] `capture_exceptions` has unused params: `log_exception`, `file_path`
- [ ] `core/__init__.py` dynamically loads empty `plugins/loader.py`
- [ ] `from sys import path` unused in `paths.py`

---

## Log

### 2026-05-17
- Set up plugin manifest system (CoreService.xml)
- Built PluginLoader with importlib.util (no sys.path hacks)
- Fixed `fetch()` missing return in api_config.py
- Fixed `.value` on enum defaults (breaks pydantic strict mode)
- Created plugin_architecture.md docs
