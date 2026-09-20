"""2. | None, and narrowing

    find_user(users, uid)   -> dict[str, str] | None
    greet_unsafe(users, uid) -> str    index straight into the result (a bug)
    greet_safe(users, uid)   -> str    narrow first; "unknown" when absent

Both take the same arguments. greet_unsafe must raise TypeError when the user
is absent — leave it broken, that is the point. greet_safe must not.

A type checker would flag greet_unsafe without running it; here the checks make
the difference visible at runtime.
"""

USERS = {"u1": {"name": "Bo"}}


def find_user(users: dict[str, dict[str, str]], uid: str) -> dict[str, str] | None:
    return users.get(uid)


def greet_unsafe(users: dict[str, dict[str, str]], uid: str) -> str:
    user = find_user(users, uid)
    return f"hello {user['name']}"      # None is not subscriptable: TypeError


def greet_safe(users: dict[str, dict[str, str]], uid: str) -> str:
    user = find_user(users, uid)
    if user is None:                    # narrowing: below here it is a dict
        return "hello unknown"
    return f"hello {user['name']}"


# ---------------------------------------------------------------- checks
# Written for you. Implement above; run the file to see where you stand.

def _run(checks):
    ok = 0
    for label, fn in checks:
        try:
            fn()
        except NotImplementedError:
            print(f"  ·     {label}"); continue
        except AssertionError as e:
            print(f"  FAIL  {label}" + (f"  — {e}" if str(e) else "")); continue
        except Exception as e:
            print(f"  ERR   {label}  — {type(e).__name__}: {e}"); continue
        print(f"  ok    {label}"); ok += 1
    print(f"{ok}/{len(checks)} passing")



import typing


def _find_user_works():
    assert find_user(USERS, "u1") == {"name": "Bo"}
    assert find_user(USERS, "nobody") is None


def _return_type_declares_none():
    r = find_user.__annotations__.get("return")
    assert r is not None, "annotate find_user's return type"
    assert type(None) in typing.get_args(r), f"it can return None; say so. Got {r!r}"


def _both_work_when_present():
    assert greet_unsafe(USERS, "u1") == "hello Bo"
    assert greet_safe(USERS, "u1") == "hello Bo"


def _unsafe_breaks_when_absent():
    try:
        greet_unsafe(USERS, "nobody")
    except TypeError:
        return
    raise AssertionError("indexing None should raise TypeError — do not guard it")


def _safe_handles_absent():
    assert greet_safe(USERS, "nobody") == "hello unknown"


if __name__ == "__main__":
    _run([
        ("find_user returns the dict or None", _find_user_works),
        ("its return type says | None",        _return_type_declares_none),
        ("both work when the user exists",     _both_work_when_present),
        ("unsafe version raises when absent",  _unsafe_breaks_when_absent),
        ("safe version narrows first",         _safe_handles_absent),
    ])
