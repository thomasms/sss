from typing import Any, Callable, Dict, Union

from functools import wraps


class SSStore:
    """A simple static store - Borg pattern"""

    __shared_state: Dict[str, Any] = {"_store": {}}

    def __init__(self) -> None:
        """Takes an no initial state. Simple Borg pattern"""
        self.__dict__ = self.__shared_state

    def set(self, key: str, result: Any) -> None:
        """Add a key value pair"""
        self._store[key] = result

    def get(self, key: str) -> Union[None, Any]:
        """Get a value given a key"""
        return self._store.get(key, None)

    def lazy_get(self, key: str) -> Callable[[], Any]:
        """Returns a function to retrieve a value"""

        def _get():
            return self.get(key)

        return _get


def keep(key: str) -> Any:
    """
    Push to in-memory static storage
    """

    def wrapped(func: Callable) -> Any:
        @wraps(func)
        def impl(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)
            store = SSStore()
            store.set(key, result)
            return result

        return impl

    return wrapped


def uses(key: str) -> Any:
    """
    Pull from in-memory static storage
    """

    def wrapped(func: Callable) -> Any:
        @wraps(func)
        def impl(*args, **kwargs) -> Any:
            store = SSStore()
            dep = store.get(key)
            result = func(*args, **{**kwargs, key: dep})
            return result

        return impl

    return wrapped


### Example


@keep("one")
def one(initial=0) -> int:
    return initial


@uses("one")
@keep("two")
def two(one=0) -> int:
    return one + 10


one(3)
two()
two()
one(4)

# -> 4
print(SSStore().get("one"))
# -> 3 + 10 = 13
print(SSStore().get("two"))
