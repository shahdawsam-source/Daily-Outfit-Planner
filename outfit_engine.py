"""Outfit suggestion logic used by the main Tkinter screen."""

import random


def _find_items(items, category, occasion, weather):
    """Return items that match category, occasion, and weather."""
    matches = []

    for item in items:
        same_category = item.get("category") == category
        occasion_ok = item.get("occasion") in (occasion, "Any")
        weather_ok = item.get("weather") in (weather, "Any")

        if same_category and occasion_ok and weather_ok:
            matches.append(item)

    return matches


def suggest_outfit(items, occasion, weather):
    """Create one outfit from available saved items."""
    tops = _find_items(items, "Top", occasion, weather)
    bottoms = _find_items(items, "Bottom", occasion, weather)
    shoes = _find_items(items, "Shoes", occasion, weather)
    outerwear = _find_items(items, "Outerwear", occasion, weather)

    missing = []
    if not tops:
        missing.append("Top")
    if not bottoms:
        missing.append("Bottom")
    if not shoes:
        missing.append("Shoes")

    if missing:
        return None, "Missing: " + ", ".join(missing)

    outfit = {
        "Top": random.choice(tops),
        "Bottom": random.choice(bottoms),
        "Shoes": random.choice(shoes),
    }

    if weather == "Cold" and outerwear:
        outfit["Outerwear"] = random.choice(outerwear)

    return outfit, None


def format_outfit(outfit):
    """Convert the outfit dictionary into readable text for the screen."""
    lines = []
    for part, item in outfit.items():
        name = item.get("name", "Unknown item")
        color = item.get("color", "No color")
        lines.append(f"{part}: {name} ({color})")

    return "\n".join(lines)
