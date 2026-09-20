# Reference — environments

Lookup card.

## A virtualenv is a directory and a `sys.path` entry

```
executable : .../project/.venv/bin/python3
prefix     : .../project/.venv
site-packages: .../project/.venv/lib/python3.11/site-packages
```

A `.venv/` holding a Python binary, a `site-packages/`, and a `pyvenv.cfg`
pointing at the base interpreter. Nothing more.

**Activating** puts `.venv/bin` first on the shell **`PATH`**, so `python`
resolves to `.venv/bin/python`. That interpreter then computes its own
`sys.path` from where it lives — `sys.prefix` is `.venv`, so *its*
site-packages is what gets searched.

**Which interpreter you launch decides which packages you can import.**
`uv run` skips activation entirely by launching the right one directly.

Two projects, two venvs, two site-packages, two different pandas. They never
meet.

### `sys.path` — what it is for

The list of directories searched, **in order**, on `import X`:

```
[0] ''  (the script's directory, or CWD)     <- FIRST
[2] .../lib/python3.11                        the standard library
[4] .../.venv/lib/python3.11/site-packages    installed packages
```

`import pandas` walks it top to bottom and stops at the first match. Everything
about imports follows: a `random.py` of yours shadows the stdlib ([0] before
[2]); a venv works because [4] changed; `import mypkg` fails from the wrong
directory because [0] changed.

---

## `pyproject.toml` — what you declare

```toml
[project]
name = "analytics"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = ["requests>=2.34.2"]

[dependency-groups]
dev = ["pytest>=9.0", "ruff>=0.9"]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

Your **intent**: what you directly use, and which versions you accept.
`requires-python` stops someone installing on 3.9 where `int | None` is a
syntax error. Dev dependencies (`uv add --dev`) are tools for developing, not
running — your users never get them.

---

## `uv.lock` — what was resolved

```
pyproject.toml:   1 dependency
uv.lock:          6 packages     certifi, charset-normalizer, idna,
                                 requests, urllib3, + your project
```

Four you never named — **transitive** dependencies. The lock pins the exact
version of every one, plus a hash.

`>=2.34.2` is a *constraint* (a set of acceptable versions). The lock is the
*answer*, frozen — so a colleague and CI get the identical environment, not
merely an acceptable one.

| buys you | |
|---|---|
| reproducibility | the same versions everywhere, months later |
| integrity | a hash mismatch is rejected; a tampered mirror cannot substitute |
| transitive pinning | your direct deps are the small problem |

**Commit the lock for an application.** A library ships no lock — its users
resolve against their own constraints, so its *version bounds* are all they get.

---

## Version constraints

```
requests              anything, including the next breaking release
requests>=2.31        2.31 or newer — no upper bound, so 3.0 is allowed
requests==2.31.0      exactly this — no patches, no security fixes
requests~=2.31.0      >=2.31.0, <2.32.0      patch only
requests~=2.31        >=2.31,   <3.0         minor + patch
```

Semver: `MAJOR.MINOR.PATCH` — patch is fixes, minor is backwards-compatible
features, major is breaking.

**The bare name is the trap.** `uv add` writes `>=X`, which is fine *for an
application* because the lock pins the real version. For a **library** add an
upper bound — `~=2.31` is the usual compromise. Pin too tightly and you miss
security fixes and conflict with everyone else's constraints.

Things that break besides a major bump: a minor release with an unintended
break (semver is a promise, not a guarantee), and a **transitive** major bump —
`urllib3` goes 3.0 under a `requests` you never touched, and the traceback has
no frames of yours.

---

## Installing your own project

Making your code findable through `sys.path` the way `pandas` is.

`uv sync` writes into site-packages:

```
_editable_impl_analytics.pth        one line: a path to your src/
analytics-0.1.0.dist-info
```

Python reads every `.pth` at startup and appends those lines to `sys.path`. So
`src/` is searched from any working directory.

**Editable install = a pointer, not a copy.** Edit the source, the change is
live. A **wheel** copies the files instead — which is why a file missing from
the wheel is genuinely missing.

```toml
[project.scripts]
analyse = "analytics.cli:main"      # gives you a real command
```

---

## Layout: flat vs `src/`

```
flat/                        src-based/
  analytics/     <- sys.path[0]   src/analytics/   <- only via the .pth
  tests/                          tests/
```

In a flat layout the package sits in the project root, which **is**
`sys.path[0]`. `import analytics` finds the *directory* — the install is
irrelevant. Uninstall it entirely and the tests still pass.

Demonstrated: exclude a module from the wheel and

```
wheel contains:   __init__.py, core.py        (no helpers.py)
tests:            1 passed
user installing:  ModuleNotFoundError: No module named 'analytics.helpers'
```

With `src/`, the project root holds nothing importable, so tests go through the
same door as users. It catches missing files, missing `__init__.py`, bad
include/exclude config, undeclared data files (a model, a CSV — common in ML),
and `from helpers import x` that only works from the source tree.

> If your tests can reach the code by a path your users cannot, you are testing
> something your users will never run.

### The cost is real

`src/` **requires installing before anything can import it**:

```
src/ layout, not installed  ->  ModuleNotFoundError: No module named 'analytics'
after uv sync               ->  1 passed
```

There is an escape hatch, and it gives up the guarantee:

```toml
[tool.pytest.ini_options]
pythonpath = ["src"]        # pytest prepends src/ itself — no install needed
```

| | cost | catches packaging bugs |
|---|---|---|
| flat | none | no |
| `src/` + install | must `uv sync` first | **yes** |
| `src/` + `pythonpath` | none | no |

The third is the layout without the benefit — a stopgap only.

**When it matters:** whenever there is a *second route* to the code — a wheel, a
Docker image, a job run from another directory, a data file loaded at runtime.
Not for a notebook repo run from its own root.

---

## uv commands

```bash
uv init                 # new project with a pyproject.toml
uv add requests         # add a dependency, update the lock, install it
uv add --dev pytest     # dev-only
uv remove requests
uv sync                 # make .venv match the lock exactly (incl. your project)
uv lock --upgrade       # re-resolve to newer versions, deliberately
uv run pytest           # run in the project env, syncing first if needed
uv run --with mypy mypy .   # one-off tool, not added to the project
uv python pin 3.11      # writes .python-version
uv build                # build a wheel + sdist into dist/
uv tool install ruff    # a global CLI tool, isolated from every project
```

`uv run` syncs first if the lock changed, which is why it "just works".

---

## The files, and what each is for

| | |
|---|---|
| `pyproject.toml` | intent — deps, metadata, tool config. **Commit.** |
| `uv.lock` | the resolved answer. **Commit** (application). |
| `.python-version` | which interpreter. **Commit.** |
| `.venv/` | the installed environment. **Never commit** — it is machine-specific and rebuildable. |
