from pathlib import Path
import shutil
from pickle import dump, load
from typing import Any, Callable, Dict, Optional, Union
from functools import wraps
import atexit
from uuid import uuid4
import pandas as pd


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


class FileStore(IStore):
    """keep it on disk"""

    def __init__(self, path: Optional[Union[None, Path]] = Path(".")) -> None:
        """Make a directory for all files in the path"""
        self.subdir = str(uuid4())
        self.store_path = path / ".sss" / self.subdir
        self.store_path.mkdir(parents=True, exist_ok=True)
        atexit.register(self.cleanup)

    def cleanup(self):
        shutil.rmtree(self.store_path)


class PickleStore(FileStore):
    """keep it on disk"""

    def _dump(self, key: str, result: Any) -> None:
        with open(self.store_path / key, "wb") as dfile:
            dump(result, dfile)

    def _load(self, key: str) -> Any:
        data = None
        with open(self.store_path / key, "rb") as dfile:
            data = load(dfile)
        return data

    def set(self, key: str, result: Any) -> None:
        """Add a key value pair"""
        self._dump(key, result)

    def get(self, key: str) -> Union[None, Any]:
        """Get a value given a key"""
        return self._load(key)


class FrameStore(FileStore):
    """Only for dataframes!"""

    def _check_type(self, result: Any) -> None:
        if not isinstance(result, pd.DataFrame):
            raise RuntimeError("FrameStore only supports dataframes!")

    def set(self, key: str, result: Any) -> None:
        """Dump to feather file format"""
        self._check_type(result)
        result: pd.DataFrame = result
        result.to_feather(self.store_path / key)

    def get(self, key: str) -> Union[None, Any]:
        """Read to feather file format"""
        # todo: check file exists
        return pd.read_feather(self.store_path / key)


def keep(key: str, store: Optional[IStore] = StupidlySimpleStore()) -> Any:
    """
    Push to in-memory static storage
    """

    def wrapped(func: Callable) -> Any:
        @wraps(func)
        def impl(*args, **kwargs) -> Any:
            result = func(*args, **kwargs)
            store.set(key, result)
            return result

        return impl

    return wrapped


def uses(
    key: str,
    argname: Optional[Union[None, str]] = None,
    store: Optional[IStore] = StupidlySimpleStore(),
) -> Any:
    """
    Pull from storage
    """

    def wrapped(func: Callable) -> Any:
        @wraps(func)
        def impl(*args, **kwargs) -> Any:
            dep = store.get(key)
            nargname = argname if argname is not None else key
            result = func(*args, **{**kwargs, nargname: dep})
            return result

        return impl

    return wrapped


### Example

# instantiate your store(s) somewhere
# probably in your __init__.py files
pickle_store = PickleStore()
simple_store = StupidlySimpleStore()
frame_store = FrameStore()


@keep("one", store=simple_store)
def one(initial=0) -> int:
    return initial


@uses("one", argname="first", store=simple_store)
@keep("two", store=pickle_store)
def two(first=0) -> int:
    return first + 10


@uses("one", argname="first", store=simple_store)
@uses("two", argname="second", store=pickle_store)
@keep("three", store=simple_store)
def three(first=0, second=0) -> int:
    return first + second


@keep("four", store=pickle_store)
def four() -> pd.DataFrame:
    return pd.DataFrame({"a": [4, 6, 10]})


@uses("four", argname="input_df", store=pickle_store)
@keep("five", store=pickle_store)
def five(input_df: pd.DataFrame = None) -> pd.DataFrame:
    df = input_df.copy()
    df["b"] = df["a"] * 3
    return df


# using ints
one(3)
two()
print(three())

# using dataframes
four()
print(five())
