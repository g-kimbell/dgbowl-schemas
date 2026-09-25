import importlib
import logging

from pydantic import ValidationError

logger = logging.getLogger(__name__)

_versions = {
    "2.2": "recipe_2_2",
    "2.1": "recipe_2_1",
    "1.0": "recipe_1_0",
}


def _load(ver: str):
    """Import a recipe model from its version."""
    return importlib.import_module(f".{_versions[ver]}", __name__).Recipe


def __getattr__(name: str):
    """Lazy import recipes and modules."""
    if name == "recipe":
        return importlib.import_module(f".{name}", __name__)
    if name == "models":
        return {ver: _load(ver) for ver in _versions}
    # Versioned aliases, e.g. Recipe_2_2.
    prefix, _, ver = name.partition("_")
    ver = ver.replace("_", ".")
    if prefix == "Recipe" and ver in _versions:
        return _load(ver)
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)


def to_recipe(**kwargs):
    firste = None
    for ver in _versions:
        Model = _load(ver)
        try:
            payload = Model(**kwargs)
            return payload
        except ValidationError as e:
            logger.info("Could not parse 'kwargs' using Recipe v%s.", ver)
            logger.info(e)
            if firste is None:
                firste = e
    raise ValueError(firste)


__all__ = [
    "recipe",
    "to_recipe",
]
