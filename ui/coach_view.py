import customtkinter as ctk

from analytics.risk_calc import get_coach_dashboard_rows

COLUMNS = [
    ("ID", 40),
    ("Name", 130),
    ("Sport", 110),
    ("Last Entry", 100),
    ("Duration (min)", 120),
    ("RPE", 55),
    ("Sleep (hrs)", 95),
    ("Soreness", 85),
    ("ACWR", 70),
    ("Status", 100),
    ("Alerts", 280),
]

STATUS_STYLES = {
    "GREEN": {"fg_color": "#1b5e20", "text_color": "#ffffff"},
    "YELLOW": {"fg_color": "#f9a825", "text_color": "#1a1a1a"},
    "RED": {"fg_color": "#b71c1c", "text_color": "#ffffff"},
    "INSUFFICIENT_DATA": {"fg_color": "#424242", "text_color": "#e0e0e0"},
}


def _display(value) -> str:
    return "—" if value is None else str(value)


class CoachDashboardView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.header = ctk.CTkLabel(self, text="Coach Dashboard", font=("Arial", 20, "bold"))
        self.header.pack(pady=(10, 0))

        self.refresh_button = ctk.CTkButton(self, text="Refresh", command=self.refresh)
        self.refresh_button.pack(pady=10)

        self.table_frame = ctk.CTkScrollableFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        for col_index, (_, width) in enumerate(COLUMNS):
            self.table_frame.grid_columnconfigure(col_index, minsize=width)

        self.refresh()

    def refresh(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self._render_header_row()

        rows = get_coach_dashboard_rows()
        if not rows:
            empty_label = ctk.CTkLabel(self.table_frame, text="No athletes found.")
            empty_label.grid(row=1, column=0, columnspan=len(COLUMNS), pady=10)
            return

        for row_index, row in enumerate(rows, start=1):
            self._render_data_row(row_index, row)

    def _render_header_row(self):
        for col_index, (label, _) in enumerate(COLUMNS):
            cell = ctk.CTkLabel(self.table_frame, text=label, font=("Arial", 13, "bold"), anchor="w")
            cell.grid(row=0, column=col_index, sticky="nsew", padx=1, pady=(0, 4))

    def _render_data_row(self, row_index: int, row: dict):
        style = STATUS_STYLES.get(row["status"], STATUS_STYLES["INSUFFICIENT_DATA"])
        alerts_text = "; ".join(row["alerts"]) if row["alerts"] else "-"

        values = [
            _display(row["athlete_id"]),
            row["name"],
            row["sport"],
            _display(row["last_entry_date"]),
            _display(row["duration_minutes"]),
            _display(row["rpe"]),
            _display(row["sleep_hours"]),
            _display(row["soreness_level"]),
            _display(row["acwr"]),
            row["status"],
            alerts_text,
        ]

        for col_index, value in enumerate(values):
            is_alerts_column = col_index == len(COLUMNS) - 1
            cell = ctk.CTkLabel(
                self.table_frame,
                text=value,
                fg_color=style["fg_color"],
                text_color=style["text_color"],
                anchor="w",
                justify="left",
                wraplength=COLUMNS[col_index][1] if is_alerts_column else 0,
                corner_radius=0,
            )
            cell.grid(row=row_index, column=col_index, sticky="nsew", padx=1, pady=1)
