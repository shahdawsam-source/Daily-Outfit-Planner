# Presentation Notes

## Problem Statement

Choosing a daily outfit can take time, especially when the user has many clothing items. The application solves this by saving wardrobe items and suggesting an outfit based on occasion and weather.

## What the App Does

The app allows the user to add clothing items, save them, view them in a table, delete items, and generate an outfit suggestion.

## Code Structure

- `main.py`: contains the Tkinter interface and buttons.
- `data_handler.py`: saves and loads data using JSON.
- `outfit_engine.py`: filters items and suggests the outfit.
- `wardrobe_data.json`: stores the saved data.

## Explanation of Git Commands

- `git add .`: prepares all changed files for saving.
- `git commit -m "message"`: saves a snapshot of the changes with a short message.
- `git push`: uploads the commits to GitHub.
- `git status`: shows what files changed.

## Short Demo Steps

1. Run `python main.py`.
2. Add one Top, one Bottom, and one Shoes item.
3. Click "Suggest outfit".
4. Show that the result appears at the bottom.
5. Close and open the app again to show that the data is still saved.
