from typing import Any, Iterable


def clear_json(dictionary: dict[str, Any], exceptions: Iterable[str] = ()) -> dict[str, Any]:
    def validate(value):
        if isinstance(value, bool):
            return True
        elif value is None:
            return False
        elif isinstance(value, str):
            return len(value)

    return {key: value for key, value in dictionary.items() if validate(value) or key in exceptions}
