import json
import pathlib
import sys

import jsonschema

_path = pathlib.Path(__file__).parent
_cache = {}


class RprMeta0(object):
    _data: dict
    version: int

    def __init__(self, data: dict):
        self._data = data
        self.version = data["version"]

    @property
    def data(self) -> dict:
        return self._data


class RprMeta1(RprMeta0):
    def __init__(self, data: dict):
        super().__init__(data)


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
        # Eventually store this in a pickle file?
        _cache[version] = res

    return res


def get_meta(data: dict) -> object:
    version = data.get("version")

    if version is None:
        raise TypeError(
            f"Given data \x1b[2m{data}\x1b[0m does not have a 'version' key."
        )

    try:
        schema = get_schema(version)
    except FileNotFoundError:
        raise ValueError(f"No schema for data version {version}.")

    # Possibly wrap in try/except
    jsonschema.validate(instance=data, schema=schema)

    cls = getattr(sys.modules[__name__], "RprMeta" + str(data["version"]), None)

    if cls is None:
        raise ValueError(
            f"Given version of metadata {data['version']} is not supported"
        )

    return cls(data)


if __name__ == "__main__":
    print(get_meta({"version": 1}))
