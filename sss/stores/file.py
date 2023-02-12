from pathlib import Path
import shutil
from pickle import dump, load
from typing import Any, Optional, Union
import atexit
from uuid import uuid4

from .base import IStore


class FileStore(IStore):
    """keep it on disk"""

    def __init__(
        self,
        path: Optional[Union[None, str, Path]] = Path("."),
        no_cleanup: Optional[bool] = False,
    ) -> None:
        """Make a directory for all files in the path"""
        self.subdir = str(uuid4())
        self.store_path = Path(path) / ".sss" / self.subdir
        self.store_path.mkdir(parents=True, exist_ok=True)
        if not no_cleanup:
            atexit.register(self.cleanup)

    def cleanup(self):
        shutil.rmtree(self.store_path)

    def _check(self, key: str) -> bool:
        return (self.store_path / key).exists()


class PickleStore(FileStore):
    """keep it on disk"""

    def _dump(self, key: str, result: Any) -> None:
        with open(self.store_path / key, "wb") as dfile:
            dump(result, dfile)

    def _load(self, key: str) -> Any:
        data = None
        if self._check(key):
            with open(self.store_path / key, "rb") as dfile:
                data = load(dfile)
        return data

    def set(self, key: str, result: Any) -> None:
        """Add a key value pair"""
        self._dump(key, result)

    def get(self, key: str) -> Union[None, Any]:
        """Get a value given a key"""
        return self._load(key)
