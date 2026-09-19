"""2. A custom exception hierarchy

    AppError(Exception)          base for everything this app raises
    ConfigError(AppError)        takes (key, message="missing"), stores .key,
                                 message reads:  config 'KEY': missing
    RetryableError(AppError)     takes (message, attempts), stores .attempts

Then classify(exc) -> "retryable" | "app" | "other", using isinstance and
ordering the checks correctly.
"""


class AppError(Exception):
    # TODO
    pass


class ConfigError(AppError):
    # TODO
    pass


class RetryableError(AppError):
    # TODO
    pass


def classify(exc):
    # TODO — most specific first
    raise NotImplementedError


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



def _config_error_shape():
    e = ConfigError("database_url")
    assert str(e) == "config 'database_url': missing", f"str() was {str(e)!r}"
    assert e.key == "database_url", "keep the key as structured data"
    assert str(ConfigError("port", "not an int")) == "config 'port': not an int"


def _retryable_shape():
    e = RetryableError("timeout", attempts=3)
    assert e.attempts == 3
    assert "timeout" in str(e)


def _base_catches_all():
    for exc in (ConfigError("k"), RetryableError("t", 1)):
        try:
            raise exc
        except AppError:
            pass
        else:
            raise AssertionError(f"{type(exc).__name__} should be caught by AppError")


def _not_too_wide():
    assert not isinstance(ValueError("x"), AppError), "AppError must not catch stdlib errors"


def _classify_orders_correctly():
    assert classify(RetryableError("t", 1)) == "retryable"
    assert classify(ConfigError("k")) == "app"
    assert classify(ValueError("v")) == "other"


if __name__ == "__main__":
    _run([
        ("ConfigError message and .key",    _config_error_shape),
        ("RetryableError carries attempts", _retryable_shape),
        ("AppError catches both subclasses", _base_catches_all),
        ("AppError does not catch ValueError", _not_too_wide),
        ("classify checks specific first",  _classify_orders_correctly),
    ])
