# importlib.util Deep Dive

> Created: 2026-05-17
> Tags: #learning #python #importlib
> Confidence: 🟡 Intermediate

---

## What Is It?

`importlib.util` is Python's stdlib module for programmatic imports. Instead of `import X` or `sys.path` hacking, you can load any `.py` file directly by its file path.

## Key Concepts

1. **Spec** — A specification object describing how to load a module (name, location, loader)
2. **Loader** — The object that actually executes the module's code
3. **Module** — The resulting Python module object, same as what `import` gives you

## How It Works

```python
import importlib.util

# Step 1: Create a spec (tells Python WHERE the module is)
spec = importlib.util.spec_from_file_location(
    "my_module",                    # name to register as
    "/path/to/my_module.py"         # actual file on disk
)

# Step 2: Create an empty module from the spec
module = importlib.util.module_from_spec(spec)

# Step 3: Execute the module's code (fills in the module)
spec.loader.exec_module(module)

# Step 4: Use it
module.some_function()
```

## Why Not Just `importlib.import_module()`?

```python
importlib.import_module("src.backend.core.paths")
```

This still relies on `sys.path` to resolve the dotted path. If your project root isn't in `sys.path`, it fails.

`spec_from_file_location` takes an **absolute file path** — no `sys.path` needed.

## `find_spec()` — Check If a Package Is Installed

```python
# Returns None if not installed, a spec if it is
spec = importlib.util.find_spec("pydantic")
if spec is None:
    print("pydantic is not installed!")
```

We use this in the PluginLoader to validate `<package>` dependencies.

## Gotchas / Pitfalls

> [!WARNING]
> `spec.loader` can be `None` if the file doesn't exist or can't be read. Always check:
> ```python
> if spec is None or spec.loader is None:
>     raise ImportError(f"Cannot load {path}")
> ```

> [!WARNING]
> `exec_module()` runs the file's top-level code. If the module has side effects at import time (like `core/__init__.py` loading plugins), they execute immediately.

> [!WARNING]
> Relative imports (`from .paths import X`) inside the loaded module will fail because the module isn't registered in a package. For modules with relative imports, you need the parent package loaded first.

## Related
- [[Plugin Architecture]]
- [[Module - Plugin Loader]]
