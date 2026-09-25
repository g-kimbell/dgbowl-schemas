import importlib
import logging

from pydantic import ValidationError

logger = logging.getLogger(__name__)

_versions = {
    "2.2": "payload_2_2",
    "2.1": "payload_2_1",
    "2.0": "payload_2_0",
    "1.0": "payload_1_0",
    "0.2": "payload_0_2",
    "0.1": "payload_0_1",
}


def _load(ver: str):
    """Import a payload model from its version."""
    return importlib.import_module(f".{_versions[ver]}", __name__).Payload


def __getattr__(name: str):
    """Lazy import payload/model."""
    if name == "payload":
        return importlib.import_module(f".{name}", __name__)
    if name == "models":
        return {ver: _load(ver) for ver in _versions}
    # Versioned aliases, e.g. Payload_2_2.
    prefix, _, ver = name.partition("_")
    ver = ver.replace("_", ".")
    if prefix == "Payload" and ver in _versions:
        return _load(ver)
    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)


def to_payload(**kwargs):
    firste = None
    for ver in _versions:
        Model = _load(ver)
        try:
            payload = Model(**kwargs)
            return payload
        except ValidationError as e:
            logger.info("Could not parse 'kwargs' using Payload-%s.", ver)
            logger.debug(e)
            if firste is None:
                firste = e
    raise ValueError(firste)


__all__ = [
    "payload",
    "to_payload",
]
