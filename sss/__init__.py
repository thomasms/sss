from pathlib import Path

from .stores.base import StupidlySimpleStore
from .stores.file import PickleStore
from .stores.frame import FrameFormat, FrameStore

from .core import keeps, uses, process

# currently supported stores
SSS_DEFAULT = StupidlySimpleStore()
SSS_PICKLE = PickleStore(path=Path("."))
SSS_FRAME = FrameStore(format=FrameFormat.feather, path=Path("."), no_cleanup=False)
