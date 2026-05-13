"""Outfit suggestion logic used by the main Tkinter screen."""

import random

REQUIRED_CATEGORIES = ("Top", "Bottom", "Shoes")


def _score_item(item, category, occasion, weather):
    """Score how well an item fits the requested outfit."""
    if item.get("category") != category:
        return None

    score = 0
    notes = []

    item_occasion = item.get("occasion", "")
    item_weather = item.get("weather", "")

    if item_occasion == occasion:
        score += 6
    elif item_occasion == "Any":
        score += 4
        notes.append("all occasions")
    else:
        notes.append(f"{item_occasion.lower()} item")

    if item_weather == weather:
        score += 5
    elif item_weather == "Any":
        score += 3
        notes.append("all weather")
    else:
        notes.append(f"{item_weather.lower()} weather")

    return score, notes


def _best_items(items, category, occasion, weather):
    """Return the highest scoring items for a category."""
    scored = []

    for item in items:
        result = _score_item(item, category, occasion, weather)
        if result is None:
            continue

        score, notes = result
        scored.append((score, notes, item))

    if not scored:
        return []

    best_score = max(score for score, _notes, _item in scored)
    return [(item, notes) for score, notes, item in scored if score == best_score]


def suggest_outfit(items, occasion, weather):
    """Create the best available outfit from saved items."""
    missing = [
        category
        for category in REQUIRED_CATEGORIES
        if not any(item.get("category") == category for item in items)
    ]

    if missing:
        return None, "Add at least one " + ", one ".join(missing) + "."

    outfit = {}
    match_notes = []

    for category in REQUIRED_CATEGORIES:
        choices = _best_items(items, category, occasion, weather)
        item, notes = random.choice(choices)
        outfit[category] = item

        if notes:
            item_name = item.get("name", category)
            match_notes.append(f"{item_name} used as best available match.")

    if weather == "Cold":
        outerwear = _best_items(items, "Outerwear", occasion, weather)
        if outerwear:
            item, notes = random.choice(outerwear)
            outfit["Outerwear"] = item
            if notes:
                item_name = item.get("name", "Outerwear")
                match_notes.append(f"{item_name} used as best available match.")

    if match_notes:
        outfit["_notes"] = match_notes

    return outfit, None


def format_outfit(outfit):
    """Convert the outfit dictionary into readable text for the screen."""
    lines = []
    for part, item in outfit.items():
        if part == "_notes":
            continue

        name = item.get("name", "Unknown item")
        color = item.get("color", "No color")
        occasion = item.get("occasion", "Any")
        weather = item.get("weather", "Any")
        lines.append(f"{part}: {name} ({color}) - {occasion}, {weather}")

    notes = outfit.get("_notes", [])
    if notes:
        lines.append("")
        lines.append("Note: Some items are best available matches.")

    return "\n".join(lines)
