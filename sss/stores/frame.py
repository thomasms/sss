"""Storage options for Dataframes"""
from pathlib import Path
from enum import Enum
from typing import Any, Callable, Dict, Optional, Tuple, Union
import pandas as pd

from .file import FileStore


class FrameFormat(Enum):
    feather = 1
    csv = 2


_MODES: Dict[str, Tuple[Callable, Callable]] = {
    FrameFormat.feather: (
        lambda key: pd.read_feather(key),
        lambda df, key: df.to_feather(key),
    ),
    FrameFormat.csv: (
        lambda key: pd.read_csv(key, sep=","),
        lambda df, key: df.to_csv(key, index=False, sep=","),
    ),
}


class FrameStore(FileStore):
    """Only for dataframes!"""

    def __init__(
        self,
        format: Optional[FrameFormat] = FrameFormat.feather,
        path: Optional[Union[None, Path]] = Path("."),
        no_cleanup: Optional[bool] = False,
    ) -> None:
        super().__init__(path, no_cleanup)
        self._modes = _MODES.get(format, FrameFormat.feather)
        self._read_func, self._write_func = self._modes

    def _check_type(self, result: Any) -> None:
        if not isinstance(result, pd.DataFrame):
            raise RuntimeError("FrameStore only supports dataframes!")

    def set(self, key: str, result: Any) -> None:
        """Dump to feather file format"""
        self._check_type(result)
        result: pd.DataFrame = result
        self._write_func(result, self.store_path / key)

    def get(self, key: str) -> Union[None, Any]:
        """Read to feather file format"""
        if not self._check(key):
            raise RuntimeError(
                f"No such key: {key} in the FrameStore. Please check you've set it in the correct store!"
            )
        return self._read_func(self.store_path / key)
