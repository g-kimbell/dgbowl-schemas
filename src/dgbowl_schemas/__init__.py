import importlib
from importlib.metadata import version

__version__ = version("dgbowl_schemas")
__all__ = ["dgpost", "yadg", "tomato"]


def __getattr__(name: str):
    """Lazy import submodules."""
    if name in __all__:
        return importlib.import_module(f".{name}", __name__)
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)
