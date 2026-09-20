"""3. Protocol

Define a Protocol `Store` requiring:

    save(self, key: str, value: str) -> None
    load(self, key: str) -> str | None

Then:
    MemoryStore     satisfies it, WITHOUT inheriting from Store
    WriteOnly       has save() but no load()
    backup(store, data) -> int    saves every item, returns how many

A type checker would reject backup(WriteOnly(), ...). At runtime it succeeds,
because backup never calls load — which is exactly why the static check matters.
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class Store(Protocol):
    def save(self, key: str, value: str) -> None: ...
    def load(self, key: str) -> str | None: ...


class MemoryStore:                      # no base class: structure is enough
    def __init__(self) -> None:
        self._data: dict[str, str] = {}

    def save(self, key: str, value: str) -> None:
        self._data[key] = value

    def load(self, key: str) -> str | None:
        return self._data.get(key)


class WriteOnly:
    def save(self, key: str, value: str) -> None:
        pass


def backup(store: Store, data: dict[str, str]) -> int:
    for key, value in data.items():
        store.save(key, value)
    return len(data)


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



def _memory_store_round_trips():
    s = MemoryStore()
    s.save("a", "1")
    assert s.load("a") == "1"
    assert s.load("missing") is None, "load should return None for an absent key"


def _satisfies_without_inheriting():
    # issubclass() on a runtime_checkable Protocol is ALSO structural, so it
    # cannot answer "did it inherit?" — look at the MRO instead.
    assert Store not in MemoryStore.__mro__, (
        f"MemoryStore must NOT inherit from Store — that is the point of a "
        f"Protocol. Its MRO is {[c.__name__ for c in MemoryStore.__mro__]}"
    )
    assert isinstance(MemoryStore(), Store), "but it should still satisfy it"


def _write_only_does_not_satisfy():
    assert not isinstance(WriteOnly(), Store), "WriteOnly has no load(); it should not satisfy Store"


def _backup_works():
    s = MemoryStore()
    assert backup(s, {"a": "1", "b": "2"}) == 2
    assert s.load("b") == "2"


def _backup_is_annotated():
    a = backup.__annotations__
    assert a.get("store") is Store, f"annotate store as Store, got {a.get('store')!r}"
    assert a.get("return") is int


def _runtime_check_is_weaker():
    s = WriteOnly()
    s.save("a", "1")
    assert backup(s, {"a": "1"}) == 1, (
        "backup only calls save, so WriteOnly works at RUNTIME — "
        "only a static checker catches the missing load()"
    )


if __name__ == "__main__":
    _run([
        ("MemoryStore round-trips",            _memory_store_round_trips),
        ("satisfies Store without inheriting", _satisfies_without_inheriting),
        ("WriteOnly does not satisfy Store",   _write_only_does_not_satisfy),
        ("backup() saves and counts",          _backup_works),
        ("backup is annotated with Store",     _backup_is_annotated),
        ("WriteOnly still works at runtime",   _runtime_check_is_weaker),
    ])
