"""Checks for the project you build in this exercise.

Build `textkit/` as described in README.md, then run this from anywhere:

    uv run python phase-00/step-0.2-working-like-an-engineer/exercises/03-environments/check_env.py

It inspects your project from the OUTSIDE — running commands against it the way
a colleague or CI would — rather than importing it into this process.
"""

import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).parent
PROJ = HERE / "textkit"


def _run(checks):
    ok = 0
    for label, fn in checks:
        try:
            fn()
        except FileNotFoundError as e:
            print(f"  ·     {label}  — {e}"); continue
        except AssertionError as e:
            print(f"  FAIL  {label}" + (f"  — {e}" if str(e) else "")); continue
        except Exception as e:
            print(f"  ERR   {label}  — {type(e).__name__}: {e}"); continue
        print(f"  ok    {label}"); ok += 1
    print(f"{ok}/{len(checks)} passing")


def uv(*args, cwd=PROJ, check=False):
    """Run a uv command inside the project."""
    r = subprocess.run(["uv", *args], cwd=cwd, capture_output=True, text=True)
    if check:
        assert r.returncode == 0, f"`uv {' '.join(args)}` failed:\n{r.stderr[-800:]}"
    return r


def _toml():
    p = PROJ / "pyproject.toml"
    if not p.exists():
        raise FileNotFoundError("textkit/pyproject.toml does not exist yet")
    return p.read_text(encoding="utf-8")


# ---------------------------------------------------------------- checks

def _src_layout():
    assert (PROJ / "src" / "textkit").is_dir(), "expected textkit/src/textkit/"
    assert not (PROJ / "textkit").is_dir(), (
        "the package must live under src/, not at the project root"
    )
    assert (PROJ / "src" / "textkit" / "__init__.py").exists(), "missing __init__.py"


def _declares_metadata():
    t = _toml()
    assert 'name = "textkit"' in t, "the project must be named textkit"
    assert "requires-python" in t, "declare requires-python"
    assert "[build-system]" in t, (
        "without a [build-system] the project cannot be installed, "
        "and src/ makes installation mandatory"
    )


def _dev_dependency_is_separate():
    t = _toml()
    assert "pytest" in t, "add pytest as a DEV dependency"
    deps = t.split("dependencies = [")[1].split("]")[0] if "dependencies = [" in t else ""
    assert "pytest" not in deps, (
        "pytest is a tool for developing, not for running — it belongs in "
        "[dependency-groups] dev, not in [project] dependencies"
    )


def _lock_exists_and_pins_more_than_you_declared():
    lock = PROJ / "uv.lock"
    if not lock.exists():
        raise FileNotFoundError("textkit/uv.lock does not exist — run `uv sync`")
    names = [l.split('"')[1] for l in lock.read_text().splitlines()
             if l.startswith("name = ")]
    assert "textkit" in names, "your own project should appear in the lock"
    assert len(names) >= 3, (
        f"the lock pins {len(names)} packages: {names}. Add a dependency with "
        "transitive dependencies of its own, so the lock has something to do."
    )


def _installed_and_importable_from_anywhere():
    uv("sync", check=True)
    with tempfile.TemporaryDirectory() as elsewhere:
        r = subprocess.run(
            ["uv", "run", "--project", str(PROJ), "python", "-c",
             "import textkit; print(textkit.__file__)"],
            cwd=elsewhere, capture_output=True, text=True,
        )
        assert r.returncode == 0, (
            f"importing textkit from another directory failed:\n{r.stderr[-600:]}"
        )
        assert "src" in r.stdout, f"imported from an unexpected place: {r.stdout.strip()}"


def _pth_file_points_at_src():
    venvs = list(PROJ.glob(".venv/lib/python*/site-packages"))
    assert venvs, "no .venv — run `uv sync`"
    pths = list(venvs[0].glob("*.pth")) + list(venvs[0].glob("__editable__*"))
    assert pths, "expected an editable-install .pth in site-packages"


def _tests_pass_without_path_hacks():
    r = uv("run", "pytest", "-q")
    assert r.returncode == 0, f"tests failed:\n{(r.stdout + r.stderr)[-900:]}"
    for f in (PROJ / "tests").glob("*.py"):
        src = f.read_text(encoding="utf-8")
        assert "sys.path" not in src, (
            f"{f.name} manipulates sys.path — an installed project does not need to"
        )
        assert "pythonpath" not in _toml(), (
            "pythonpath in pytest config bypasses the install; remove it"
        )


def _script_entry_point_works():
    assert "[project.scripts]" in _toml(), "declare a console script"
    r = uv("run", "wordcount", "--", "hello hello world")
    assert r.returncode == 0, f"`uv run wordcount` failed:\n{r.stderr[-600:]}"
    out = r.stdout.strip()
    assert "hello" in out and "2" in out, f"unexpected output: {out!r}"


def _wheel_contains_every_module():
    uv("build", check=True)
    wheels = sorted((PROJ / "dist").glob("*.whl"))
    assert wheels, "no wheel in dist/ — run `uv build`"
    import zipfile
    packaged = {n.split("/")[-1] for n in zipfile.ZipFile(wheels[-1]).namelist()
                if n.endswith(".py")}
    on_disk = {p.name for p in (PROJ / "src" / "textkit").glob("*.py")}
    missing = on_disk - packaged
    assert not missing, (
        f"these modules are in src/ but NOT in the wheel: {sorted(missing)}. "
        "A user installing it would get ModuleNotFoundError."
    )


if __name__ == "__main__":
    if shutil.which("uv") is None:
        sys.exit("uv is not on PATH")
    _run([
        ("src/ layout, package under src/textkit",   _src_layout),
        ("pyproject declares name, python, build",   _declares_metadata),
        ("pytest is a DEV dependency, not a runtime one", _dev_dependency_is_separate),
        ("uv.lock exists and pins transitives",      _lock_exists_and_pins_more_than_you_declared),
        ("importable from any directory",            _installed_and_importable_from_anywhere),
        ("an editable .pth points at src/",          _pth_file_points_at_src),
        ("tests pass with no sys.path hacks",        _tests_pass_without_path_hacks),
        ("`uv run wordcount` works",                 _script_entry_point_works),
        ("the wheel contains every module in src/",  _wheel_contains_every_module),
    ])
