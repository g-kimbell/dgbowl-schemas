import importlib
import logging

from pydantic import ValidationError

logger = logging.getLogger(__name__)

# Version -> (submodule, whether it defines a separate Metadata model).
_versions = {
    "7.0": ("dataschema_7_0", False),
    "6.0": ("dataschema_6_0", False),
    "5.1": ("dataschema_5_1", False),
    "5.0": ("dataschema_5_0", True),
    "4.2": ("dataschema_4_2", True),
    "4.1": ("dataschema_4_1", True),
    "4.0": ("dataschema_4_0", True),
    "3.1": ("dataschema_3_1", False),
}


def _load(ver: str):
    """Import a (DataSchema, Metadata) from its version."""
    name, has_metadata = _versions[ver]
    mod = importlib.import_module(f".{name}", __name__)
    return mod.DataSchema, mod.Metadata if has_metadata else None


def __getattr__(name):
    """Lazy import dataschema/models."""
    if name == "dataschema":
        return importlib.import_module(f".{name}", __name__)
    if name == "models":
        return {ver: _load(ver) for ver in _versions}
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def to_dataschema(**kwargs):
    # figure out matching Metadata -> identify correct Model:
    errors = ["Could not parse 'kwargs['metadata']' using any Metadata!", ""]
    for ver in _versions:
        Model, Metadata = _load(ver)
        try:
            if Metadata is None:
                schema = Model(**kwargs)
                return schema
            else:
                Metadata(**kwargs.get("metadata", {}))
                break
        except ValidationError as e:
            errors.append(
                f"Could not parse 'kwargs['metadata']' using Metadata v{ver}:"
            )
            errors += str(e).replace("\n", "\n ").split("\n")
            errors.append("")
    else:
        raise ValueError("\n".join(errors))

    logger.debug("Identified 'kwargs['metadata']' as Metadata v%s.", ver)

    # attempt to parse using identified Model
    schema = Model(**kwargs)
    return schema


__all__ = [
    "dataschema",
    "to_dataschema",
]
