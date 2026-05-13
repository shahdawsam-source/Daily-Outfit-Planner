import tkinter as tk
from tkinter import messagebox, ttk

from data_handler import load_items, save_items
from outfit_engine import format_outfit, suggest_outfit


CATEGORIES = ("Top", "Bottom", "Shoes", "Outerwear")
OCCASIONS = ("University", "Casual", "Formal", "Sport", "Any")
WEATHER = ("Hot", "Mild", "Cold", "Any")
FILTER_OCCASIONS = ("University", "Casual", "Formal", "Sport")
FILTER_WEATHER = ("Hot", "Mild", "Cold")


class WardrobeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Outfit Planner")
        self.root.geometry("960x650")
        self.root.minsize(900, 620)

        self.items = load_items()

        self.name_var = tk.StringVar()
        self.category_var = tk.StringVar(value="Top")
        self.color_var = tk.StringVar()
        self.occasion_var = tk.StringVar(value="University")
        self.weather_var = tk.StringVar(value="Mild")

        self.filter_occasion_var = tk.StringVar(value="University")
        self.filter_weather_var = tk.StringVar(value="Mild")
        self.result_var = tk.StringVar(value="Choose an occasion and weather, then suggest an outfit.")
        self.status_var = tk.StringVar()

        self._configure_styles()
        self._build_screen()
        self._bind_changes()
        self._refresh_table()
        self._update_status()

    def _configure_styles(self):
        self.root.configure(bg="#eef1f5")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 10), background="#eef1f5")
        style.configure("Title.TLabel", font=("Segoe UI", 24, "bold"), foreground="#172033")
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10), foreground="#5a6475")
        style.configure("Panel.TLabelframe", background="#ffffff", bordercolor="#d8dee8", relief="solid")
        style.configure("Panel.TLabelframe.Label", background="#ffffff", foreground="#172033", font=("Segoe UI", 10, "bold"))
        style.configure("Panel.TFrame", background="#ffffff")
        style.configure("TLabel", background="#ffffff", foreground="#172033")
        style.configure("TEntry", padding=5, fieldbackground="#ffffff")
        style.configure("TCombobox", padding=5, fieldbackground="#ffffff")
        style.configure("Primary.TButton", padding=(16, 8), background="#1f5f9f", foreground="#ffffff")
        style.map("Primary.TButton", background=[("active", "#174a7d")])
        style.configure("Danger.TButton", padding=(16, 8), background="#a03434", foreground="#ffffff")
        style.map("Danger.TButton", background=[("active", "#7f2626")])
        style.configure("Treeview", rowheight=30, background="#ffffff", fieldbackground="#ffffff")
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#e5eaf1", foreground="#172033")

    def _build_screen(self):
        shell = ttk.Frame(self.root, padding=22)
        shell.pack(fill="both", expand=True)
        shell.columnconfigure(0, weight=1)
        shell.rowconfigure(1, weight=1)

        header = ttk.Frame(shell)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        header.columnconfigure(0, weight=1)

        ttk.Label(header, text="Daily Outfit Planner", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text="Build a wardrobe, then get the best outfit available for the day.",
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

        content = ttk.Frame(shell)
        content.grid(row=1, column=0, sticky="nsew")
        content.columnconfigure(0, weight=0)
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)
        content.rowconfigure(1, weight=0)

        self._build_form(content)
        self._build_table(content)
        self._build_generator(content)

        ttk.Label(shell, textvariable=self.status_var, style="Subtitle.TLabel").grid(row=2, column=0, sticky="w", pady=(12, 0))

    def _build_form(self, parent):
        panel = ttk.LabelFrame(parent, text="Add clothing item", style="Panel.TLabelframe", padding=16)
        panel.grid(row=0, column=0, sticky="nsw", padx=(0, 18))
        panel.columnconfigure(1, weight=1)

        fields = (
            ("Item name", ttk.Entry(panel, textvariable=self.name_var, width=26)),
            ("Category", ttk.Combobox(panel, textvariable=self.category_var, values=CATEGORIES, state="readonly", width=24)),
            ("Color", ttk.Entry(panel, textvariable=self.color_var, width=26)),
            ("Occasion", ttk.Combobox(panel, textvariable=self.occasion_var, values=OCCASIONS, state="readonly", width=24)),
            ("Weather", ttk.Combobox(panel, textvariable=self.weather_var, values=WEATHER, state="readonly", width=24)),
        )

        for row, (label, widget) in enumerate(fields):
            ttk.Label(panel, text=label).grid(row=row, column=0, sticky="w", pady=7, padx=(0, 12))
            widget.grid(row=row, column=1, sticky="ew", pady=7)

        ttk.Button(panel, text="Add item", command=self.add_item, style="Primary.TButton").grid(
            row=5, column=0, columnspan=2, sticky="ew", pady=(18, 8)
        )
        ttk.Button(panel, text="Delete selected item", command=self.delete_selected, style="Danger.TButton").grid(
            row=6, column=0, columnspan=2, sticky="ew"
        )

    def _build_table(self, parent):
        panel = ttk.LabelFrame(parent, text="Saved wardrobe", style="Panel.TLabelframe", padding=12)
        panel.grid(row=0, column=1, sticky="nsew")
        panel.rowconfigure(0, weight=1)
        panel.columnconfigure(0, weight=1)

        columns = ("name", "category", "color", "occasion", "weather")
        self.table = ttk.Treeview(panel, columns=columns, show="headings", selectmode="browse")
        headings = {
            "name": ("Name", 170),
            "category": ("Category", 95),
            "color": ("Color", 95),
            "occasion": ("Occasion", 115),
            "weather": ("Weather", 95),
        }

        for column, (label, width) in headings.items():
            self.table.heading(column, text=label)
            self.table.column(column, width=width, minwidth=75, anchor="w")

        scrollbar = ttk.Scrollbar(panel, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)
        self.table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.table.tag_configure("odd", background="#f7f9fc")
        self.table.tag_configure("even", background="#ffffff")

    def _build_generator(self, parent):
        panel = ttk.LabelFrame(parent, text="Generate outfit", style="Panel.TLabelframe", padding=16)
        panel.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(18, 0))
        panel.columnconfigure(5, weight=1)

        ttk.Label(panel, text="Occasion").grid(row=0, column=0, sticky="w", padx=(0, 8))
        ttk.Combobox(
            panel,
            textvariable=self.filter_occasion_var,
            values=FILTER_OCCASIONS,
            state="readonly",
            width=16,
        ).grid(row=0, column=1, sticky="w", padx=(0, 18))

        ttk.Label(panel, text="Weather").grid(row=0, column=2, sticky="w", padx=(0, 8))
        ttk.Combobox(
            panel,
            textvariable=self.filter_weather_var,
            values=FILTER_WEATHER,
            state="readonly",
            width=16,
        ).grid(row=0, column=3, sticky="w", padx=(0, 18))

        ttk.Button(panel, text="Suggest outfit", command=self.generate_outfit, style="Primary.TButton").grid(
            row=0, column=4, sticky="w"
        )

        result_box = ttk.Frame(panel, style="Panel.TFrame", padding=(0, 14, 0, 0))
        result_box.grid(row=1, column=0, columnspan=6, sticky="ew")
        result_box.columnconfigure(0, weight=1)

        self.result_label = ttk.Label(
            result_box,
            textvariable=self.result_var,
            background="#f7f9fc",
            foreground="#172033",
            padding=14,
            justify="left",
            anchor="w",
        )
        self.result_label.grid(row=0, column=0, sticky="ew")

    def _bind_changes(self):
        self.filter_occasion_var.trace_add("write", self._clear_result)
        self.filter_weather_var.trace_add("write", self._clear_result)
        self.root.bind("<Return>", lambda _event: self.add_item())

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
        self._update_status()
        self._clear_result()

        self.name_var.set("")
        self.color_var.set("")
        self.name_var.focus_set()

    def delete_selected(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select an item first.")
            return

        row_index = self.table.index(selected[0])
        removed = self.items.pop(row_index)
        save_items(self.items)
        self._refresh_table()
        self._update_status()
        self._clear_result()
        self.status_var.set(f"Deleted {removed.get('name', 'selected item')}.")

    def generate_outfit(self):
        occasion = self.filter_occasion_var.get()
        weather = self.filter_weather_var.get()
        outfit, error = suggest_outfit(self.items, occasion, weather)

        if error:
            messagebox.showwarning("Cannot generate outfit", error)
            return

        self.result_var.set(f"Best outfit for {occasion} / {weather}\n\n{format_outfit(outfit)}")

    def _clear_result(self, *_args):
        self.result_var.set("Filters changed. Suggest an outfit to see the newest match.")

    def _refresh_table(self):
        for row in self.table.get_children():
            self.table.delete(row)

        for index, item in enumerate(self.items):
            tag = "even" if index % 2 == 0 else "odd"
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
                tags=(tag,),
            )

    def _update_status(self):
        counts = {category: 0 for category in CATEGORIES}
        for item in self.items:
            category = item.get("category")
            if category in counts:
                counts[category] += 1

        self.status_var.set(
            f"{len(self.items)} items saved | "
            f"Tops: {counts['Top']} | Bottoms: {counts['Bottom']} | "
            f"Shoes: {counts['Shoes']} | Outerwear: {counts['Outerwear']}"
        )


if __name__ == "__main__":
    window = tk.Tk()
    app = WardrobeApp(window)
    window.mainloop()
