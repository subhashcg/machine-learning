"""Checks on YOUR test suite. Run this after your tests pass.

    uv run python phase-00/step-0.2-working-like-an-engineer/exercises/01-pytest/meta_check.py

It runs pytest on test_textstats.py, then inspects the file's source to confirm
you used the features the brief asked for.
"""

import ast
import pathlib
import re
import subprocess
import sys

HERE = pathlib.Path(__file__).parent
SUITE = HERE / "test_textstats.py"


def _run(checks):
    ok = 0
    for label, fn in checks:
        try:
            fn()
        except AssertionError as e:
            print(f"  FAIL  {label}" + (f"  — {e}" if str(e) else "")); continue
        except Exception as e:
            print(f"  ERR   {label}  — {type(e).__name__}: {e}"); continue
        print(f"  ok    {label}"); ok += 1
    print(f"{ok}/{len(checks)} passing")


_result = subprocess.run(
    [sys.executable, "-m", "pytest", str(SUITE), "-q", "--no-header"],
    capture_output=True, text=True, cwd=HERE,
)
_out = _result.stdout + _result.stderr
_raw = SUITE.read_text(encoding="utf-8")
_tree = ast.parse(_raw)

# strip the module docstring, so the brief's own text cannot satisfy a check
_lines = _raw.splitlines(keepends=True)
if (_tree.body and isinstance(_tree.body[0], ast.Expr)
        and isinstance(_tree.body[0].value, ast.Constant)
        and isinstance(_tree.body[0].value.value, str)):
    _doc_end = _tree.body[0].end_lineno
    _src = "".join(_lines[_doc_end:])
else:
    _src = _raw
_funcs = [n for n in ast.walk(_tree)
          if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")]


def _suite_passes():
    assert _result.returncode == 0, f"pytest failed:\n{_out[-1500:]}"
    assert "no tests ran" not in _out, "no tests were collected"


def _enough_tests():
    assert len(_funcs) >= 8, f"found {len(_funcs)} test functions, want at least 8"


def _uses_parametrize():
    cases = 0
    for fn in _funcs:
        for dec in fn.decorator_list:
            if "parametrize" in ast.dump(dec):
                for node in ast.walk(dec):
                    if isinstance(node, ast.List) and node.elts:
                        cases = max(cases, len(node.elts))
    assert cases >= 4, f"largest parametrize has {cases} cases, want at least 4"


def _parametrize_covers_edges():
    found = False
    for fn in _funcs:
        for dec in fn.decorator_list:
            if "parametrize" in ast.dump(dec):
                for node in ast.walk(dec):
                    if isinstance(node, ast.Constant) and node.value == "":
                        found = True
    assert found, "include the empty string as a parametrize case"


def _uses_raises_with_match():
    assert "pytest.raises" in _src, "use pytest.raises for average_length([])"
    assert re.search(r"pytest\.raises\([^)]*match\s*=", _src), (
        "pass match= so a ValueError raised for another reason cannot pass"
    )


def _uses_approx():
    assert "pytest.approx" in _src, "average_length returns a float — use approx"


def _has_a_fixture_used_twice():
    fixtures = [n.name for n in ast.walk(_tree)
                if isinstance(n, ast.FunctionDef)
                and any("fixture" in ast.dump(d) for d in n.decorator_list)]
    assert fixtures, "define a fixture that builds a file with tmp_path"
    assert any("tmp_path" in [a.arg for a in n.args.args]
               for n in ast.walk(_tree)
               if isinstance(n, ast.FunctionDef) and n.name in fixtures), (
        "the fixture should take tmp_path"
    )
    used = {f: sum(1 for t in _funcs if f in [a.arg for a in t.args.args])
            for f in fixtures}
    assert max(used.values(), default=0) >= 2, (
        f"a fixture should be used by at least two tests; usage: {used}"
    )


def _tests_the_missing_file():
    assert "FileNotFoundError" in _src, "test load_words on a path that does not exist"


def _pins_down_tie_breaking():
    assert "top_n" in _src, "test top_n"
    assert re.search(r"tie", _src, re.I), (
        "pin down what top_n does when two words have the same count, "
        "and mention 'tie' in a test name or comment"
    )


if __name__ == "__main__":
    print(_out.strip().splitlines()[-1] if _out.strip() else "(pytest produced no output)")
    print()
    _run([
        ("your test suite passes",              _suite_passes),
        ("at least 8 test functions",           _enough_tests),
        ("a parametrize with 4+ cases",         _uses_parametrize),
        ("the empty string is one of them",     _parametrize_covers_edges),
        ("pytest.raises with match=",           _uses_raises_with_match),
        ("pytest.approx used",                  _uses_approx),
        ("a tmp_path fixture, used twice",      _has_a_fixture_used_twice),
        ("load_words on a missing file",        _tests_the_missing_file),
        ("top_n tie-breaking pinned down",      _pins_down_tie_breaking),
    ])
