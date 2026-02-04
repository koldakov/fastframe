from importlib.metadata import PackageMetadata
from importlib.metadata import metadata as _metadata

__all__ = [
    "metadata",
]


metadata: PackageMetadata = _metadata("fastframe")
