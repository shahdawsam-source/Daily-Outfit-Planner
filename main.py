import tkinter as tk
from tkinter import messagebox, ttk

from data_handler import load_items, save_items
from outfit_engine import format_outfit, suggest_outfit


class WardrobeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Outfit Planner")
        self.root.geometry("820x560")
        self.root.resizable(False, False)

        self.items = load_items()

        self.name_var = tk.StringVar()
        self.category_var = tk.StringVar(value="Top")
        self.color_var = tk.StringVar()
        self.occasion_var = tk.StringVar(value="University")
        self.weather_var = tk.StringVar(value="Mild")

        self.filter_occasion_var = tk.StringVar(value="University")
        self.filter_weather_var = tk.StringVar(value="Mild")

        self._build_screen()
        self._refresh_table()

    def _build_screen(self):
        title = tk.Label(
            self.root,
            text="Daily Outfit Planner",
            font=("Arial", 20, "bold"),
            pady=12,
        )
        title.pack()

        container = tk.Frame(self.root, padx=14, pady=8)
        container.pack(fill="both", expand=True)

        left = tk.LabelFrame(container, text="Add clothing item", padx=12, pady=12)
        left.place(x=10, y=10, width=300, height=360)

        tk.Label(left, text="Item name").grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(left, textvariable=self.name_var, width=28).grid(row=0, column=1, pady=5)

        tk.Label(left, text="Category").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Combobox(
            left,
            textvariable=self.category_var,
            values=["Top", "Bottom", "Shoes", "Outerwear"],
            state="readonly",
            width=25,
        ).grid(row=1, column=1, pady=5)

        tk.Label(left, text="Color").grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(left, textvariable=self.color_var, width=28).grid(row=2, column=1, pady=5)

        tk.Label(left, text="Occasion").grid(row=3, column=0, sticky="w", pady=5)
        ttk.Combobox(
            left,
            textvariable=self.occasion_var,
            values=["University", "Casual", "Formal", "Sport", "Any"],
            state="readonly",
            width=25,
        ).grid(row=3, column=1, pady=5)

        tk.Label(left, text="Weather").grid(row=4, column=0, sticky="w", pady=5)
        ttk.Combobox(
            left,
            textvariable=self.weather_var,
            values=["Hot", "Mild", "Cold", "Any"],
            state="readonly",
            width=25,
        ).grid(row=4, column=1, pady=5)

        tk.Button(
            left,
            text="Add item",
            command=self.add_item,
            width=22,
            bg="#2e7d32",
            fg="white",
        ).grid(row=5, column=0, columnspan=2, pady=14)

        tk.Button(
            left,
            text="Delete selected item",
            command=self.delete_selected,
            width=22,
            bg="#9e2a2b",
            fg="white",
        ).grid(row=6, column=0, columnspan=2, pady=3)

        right = tk.LabelFrame(container, text="Saved wardrobe", padx=10, pady=10)
        right.place(x=330, y=10, width=465, height=360)

        columns = ("name", "category", "color", "occasion", "weather")
        self.table = ttk.Treeview(right, columns=columns, show="headings", height=13)
        self.table.heading("name", text="Name")
        self.table.heading("category", text="Category")
        self.table.heading("color", text="Color")
        self.table.heading("occasion", text="Occasion")
        self.table.heading("weather", text="Weather")

        self.table.column("name", width=120)
        self.table.column("category", width=80)
        self.table.column("color", width=75)
        self.table.column("occasion", width=95)
        self.table.column("weather", width=75)
        self.table.pack(fill="both", expand=True)

        bottom = tk.LabelFrame(container, text="Generate outfit", padx=12, pady=12)
        bottom.place(x=10, y=385, width=785, height=120)

        tk.Label(bottom, text="Occasion").grid(row=0, column=0, padx=6)
        ttk.Combobox(
            bottom,
            textvariable=self.filter_occasion_var,
            values=["University", "Casual", "Formal", "Sport"],
            state="readonly",
            width=14,
        ).grid(row=0, column=1, padx=6)

        tk.Label(bottom, text="Weather").grid(row=0, column=2, padx=6)
        ttk.Combobox(
            bottom,
            textvariable=self.filter_weather_var,
            values=["Hot", "Mild", "Cold"],
            state="readonly",
            width=14,
        ).grid(row=0, column=3, padx=6)

        tk.Button(
            bottom,
            text="Suggest outfit",
            command=self.generate_outfit,
            width=18,
            bg="#1d4e89",
            fg="white",
        ).grid(row=0, column=4, padx=12)

        self.result_label = tk.Label(
            bottom,
            text="Add a few items, then generate an outfit.",
            justify="left",
            font=("Arial", 10),
        )
        self.result_label.grid(row=1, column=0, columnspan=5, sticky="w", pady=10)

    def add_item(self):
        name = self.name_var.get().strip()
        color = self.color_var.get().strip()

        if not name or not color:
            messagebox.showwarning("Missing data", "Please enter both item name and color.")
            return

        item = {
            "name": name,
            "category": self.category_var.get(),
            "color": color,
            "occasion": self.occasion_var.get(),
            "weather": self.weather_var.get(),
        }

        self.items.append(item)
        save_items(self.items)
        self._refresh_table()

        self.name_var.set("")
        self.color_var.set("")
        messagebox.showinfo("Saved", "Item added successfully.")

    def delete_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select an item first.")
            return

        row_index = self.table.index(selected[0])
        self.items.pop(row_index)
        save_items(self.items)
        self._refresh_table()

    def generate_outfit(self):
        outfit, error = suggest_outfit(
            self.items,
            self.filter_occasion_var.get(),
            self.filter_weather_var.get(),
        )

        if error:
            messagebox.showwarning("Cannot generate outfit", error)
            return

        self.result_label.config(text=format_outfit(outfit))

    def _refresh_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for item in self.items:
            self.table.insert(
                "",
                tk.END,
                values=(
                    item.get("name", ""),
                    item.get("category", ""),
                    item.get("color", ""),
                    item.get("occasion", ""),
                    item.get("weather", ""),
                ),
            )


if __name__ == "__main__":
    window = tk.Tk()
    app = WardrobeApp(window)
    window.mainloop()
