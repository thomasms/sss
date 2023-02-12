"""Core functionality - decorators"""
from typing import Any, Callable, Optional, Iterable, Union
from functools import wraps

from .stores.base import IStore, StupidlySimpleStore


def keeps(key: str, store: Optional[IStore] = StupidlySimpleStore()) -> Any:
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


def process(steps: Iterable[Callable[[], Any]]) -> Any:
    """Sequentially run through steps"""
    last = None
    for step in steps:
        last = step()
    return last
