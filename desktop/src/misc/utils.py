from typing import Any


def clear_json(dictionary: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in dictionary.items() if value and len(value)}
