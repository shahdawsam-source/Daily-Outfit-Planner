"""Small helper functions for saving and reading wardrobe items."""

import json
from pathlib import Path

DATA_FILE = Path("wardrobe_data.json")


def load_items():
    """Read items from the JSON file. If the file is missing, start empty."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
    except json.JSONDecodeError:
        # If the file was edited wrongly, the app should not crash.
        return []

    return []


def save_items(items):
    """Save the current wardrobe list to the JSON file."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(items, file, indent=4, ensure_ascii=False)
