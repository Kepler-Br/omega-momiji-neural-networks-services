from typing import Optional


def get_dict_key_by_path(dictionary: dict, path: str, fail: bool = True) -> Optional[str | dict | int | float | bool]:
    try:
        value = dictionary
        for key in path.split('.'):
            value = value[key]
    except KeyError as e:
        if fail:
            raise KeyError(f"Key {path} not found in config file") from e
        else:
            return None
    return value
