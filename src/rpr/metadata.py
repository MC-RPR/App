import json
import pathlib

import jsonschema

_path = pathlib.Path(__file__).parent
_cache = {}


class RprMeta(object):
    pass


class RprMeta1(RprMeta):
    pass


def get_schema(version: int, use_cache: bool = True) -> dict:
    if use_cache and version in _cache:
        return _cache[version]

    schema_path = _path.joinpath(f"data/rpr{version}.schema.json")

    if not schema_path.exists():
        raise FileNotFoundError(
            f"Cannot find schema version {version} at '{schema_path}'."
        )

    with open(schema_path, "rt") as fp:
        res = json.load(fp)

    if use_cache and version not in _cache:
        _cache[version] = res

    return res


def get_meta(data: dict) -> RprMeta:
    version = data.get("version")

    if version is None:
        raise TypeError(
            f"Given data \x1b[2m{data}\x1b[0m does not have a 'version' key."
        )

    try:
        schema = get_schema(version)
    except FileNotFoundError:
        raise TypeError(f"No schema for data version {version}.")

    # Validate
