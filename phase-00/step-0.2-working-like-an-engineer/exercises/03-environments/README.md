# Exercises — Topic 3, environments

One exercise: **build a real installable project from nothing.**

```bash
cd phase-00/step-0.2-working-like-an-engineer/exercises/03-environments
uv run python check_env.py
```

`check_env.py` inspects your project **from the outside** — it runs `uv sync`,
`uv build`, and `uv run` against it the way a colleague or CI would, rather than
importing it into its own process. That is the point of the topic.

---

## Build `textkit/`

A small word-counting package, in `textkit/` next to this file:

```
textkit/
  pyproject.toml
  src/textkit/
    __init__.py
    core.py           word_count(text) -> dict[str, int]
    cli.py            a console entry point
  tests/
    test_core.py
```

## What the checks require

| | |
|---|---|
| **`src/` layout** | the package under `src/textkit/`, nothing importable at the project root |
| **metadata** | `name = "textkit"`, `requires-python`, and a `[build-system]` — without one it cannot be installed, and `src/` makes installation mandatory |
| **a real dependency** | one with transitive dependencies of its own, so the lock has something to do. `click` is a reasonable choice for a CLI. |
| **pytest as a dev dependency** | `uv add --dev pytest` — it belongs in `[dependency-groups]`, not `[project] dependencies` |
| **`uv.lock`** | committed, pinning your project plus its transitives |
| **importable from anywhere** | a check imports it from a temp directory |
| **an editable `.pth`** | proof the install is a pointer at `src/`, not a copy |
| **no `sys.path` hacks** | and no `pythonpath` in the pytest config — an installed project needs neither |
| **`uv run wordcount`** | a `[project.scripts]` entry point; given `"hello hello world"` it prints each word and its count |
| **the wheel is complete** | `uv build`, then every `.py` in `src/textkit/` must be inside it |

## The one that catches people

The last check builds a wheel and compares its contents against `src/`. If a
module is on disk but missing from the wheel, a user installing it gets
`ModuleNotFoundError` — and your tests would never have noticed.

That is the whole argument for `src/`, made concrete against your own code.

## Suggested order

```bash
mkdir -p textkit/src/textkit textkit/tests
cd textkit
uv init --bare          # or write pyproject.toml by hand
uv add click
uv add --dev pytest
# ...write the code...
uv sync
uv run pytest
uv build
```

Then run `check_env.py` from the parent directory.

Do not commit `textkit/.venv/` or `textkit/dist/` — both are rebuildable.
