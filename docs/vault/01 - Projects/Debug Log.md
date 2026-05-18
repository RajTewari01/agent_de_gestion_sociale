# Debug Log

> Tags: #debug #log
> Project: [[Agent de Gestion Sociale]]

---

## 2026-05-17

### 🟢 RESOLVED — `fetch()` returns None for valid keys
- **File**: `core/api_config.py:22-32`
- **Symptom**: `fetch()` returns `None` when key exists in `model_extra`
- **Root Cause**: Missing `return SecretStr(val)` at end of function
- **Fix**: Added `return SecretStr(val)` after the `if not val` checks
- **Details**: [[Debug - fetch returns None]]

### 🟢 RESOLVED — Pydantic strict mode + enum .value
- **File**: `config/dev.py:6`, `config/prod.py:6`
- **Symptom**: `ValidationError` on `DevConfig()` / `ProdConfig()` instantiation
- **Root Cause**: Using `ProductionVariable.DEVELOPMENT.value` (a string) with `strict=True` (no coercion)
- **Fix**: Removed `.value` — pass enum member directly
- **Details**: [[Debug - Pydantic Strict Enum]]

---

## Template

### Status — Short description
- **File**: 
- **Symptom**: 
- **Root Cause**: 
- **Fix**: 
- **Details**: [[]]
