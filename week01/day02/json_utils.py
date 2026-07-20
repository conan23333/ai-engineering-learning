import json
from typing import Any


def load_json(file_path: str) -> Any:
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(data: Any, file_path: str) -> None:

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )