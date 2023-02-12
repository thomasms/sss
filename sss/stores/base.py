from typing import Any, Callable, Dict, Union


class IStore:
    """A simple interface to the store"""

    def set(self, key: str, result: Any) -> None:
        """Add a key value pair"""
        pass

    def get(self, key: str) -> Union[None, Any]:
        """Get a value given a key"""
        return None

    def lazy_get(self, key: str) -> Callable[[], Any]:
        """Returns a function to retrieve a value"""

        def _get():
            return self.get(key)

        return _get


class StupidlySimpleStore(IStore):
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
