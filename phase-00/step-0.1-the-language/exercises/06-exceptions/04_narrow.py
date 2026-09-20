"""4. Catch only what you can act on

Two versions of the same lookup over a dict-of-dicts.

    wide(data, uid)    the antipattern: except Exception -> return None
    narrow(data, uid)  returns None ONLY when the user is genuinely absent;
                       everything else propagates

`data` is expected to look like {"users": {"u1": {...}}}. If it does not — a
missing "users" key, or a value that is not a dict — that is a caller bug and
should raise, not become None.
"""


def wide(data, uid):
    try:
        return data["users"][uid]
    except Exception:           # also catches the caller's bugs, and any typo in here
        return None


def narrow(data, uid):
    users = data["users"]       # outside the try: a missing "users" key is a caller bug
    try:
        return users[uid]       # a list here raises TypeError, which propagates
    except KeyError:            # the one case we can act on: no such user
        return None


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



GOOD = {"users": {"u1": {"name": "Bo"}}}
NO_USERS_KEY = {"accounts": {}}
USERS_IS_A_LIST = {"users": ["u1"]}


def _both_find_a_user():
    assert wide(GOOD, "u1") == {"name": "Bo"}
    assert narrow(GOOD, "u1") == {"name": "Bo"}


def _both_return_none_for_absent_user():
    assert wide(GOOD, "nobody") is None
    assert narrow(GOOD, "nobody") is None


def _wide_hides_a_malformed_payload():
    assert wide(NO_USERS_KEY, "u1") is None, "the wide version swallows it"
    assert wide(USERS_IS_A_LIST, "u1") is None, "the wide version swallows it"


def _narrow_lets_malformed_payloads_raise():
    for bad, why in [(NO_USERS_KEY, "missing 'users' key"), (USERS_IS_A_LIST, "'users' is a list")]:
        try:
            narrow(bad, "u1")
        except Exception:
            continue
        raise AssertionError(f"narrow() should raise when {why}, not return None")


if __name__ == "__main__":
    _run([
        ("both find an existing user",          _both_find_a_user),
        ("both return None for an absent user", _both_return_none_for_absent_user),
        ("wide() hides a malformed payload",    _wide_hides_a_malformed_payload),
        ("narrow() lets malformed payloads raise", _narrow_lets_malformed_payloads_raise),
    ])
