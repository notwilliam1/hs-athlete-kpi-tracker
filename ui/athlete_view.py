import customtkinter as ctk
from datetime import date, datetime

from database.db_engine import get_session
from database.models import Athlete, DailyLog

MIN_DURATION_MINUTES = 1
MAX_DURATION_MINUTES = 600
MIN_RPE = 1
MAX_RPE = 10
MIN_SLEEP_HOURS = 0.0
MAX_SLEEP_HOURS = 24.0
MIN_SORENESS = 1
MAX_SORENESS = 5


class AthleteCheckInView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(self, text="Athlete Check-In", font=("Arial", 20, "bold"))
        self.label.pack(pady=10)

        self.athlete_id_entry = ctk.CTkEntry(self, placeholder_text="Athlete ID")
        self.athlete_id_entry.pack(pady=5)

        self.entry_date_entry = ctk.CTkEntry(self, placeholder_text="Date (YYYY-MM-DD, blank = today)")
        self.entry_date_entry.pack(pady=5)

        self.duration_entry = ctk.CTkEntry(self, placeholder_text="Duration (minutes)")
        self.duration_entry.pack(pady=5)

        self.rpe_entry = ctk.CTkEntry(self, placeholder_text="RPE (1-10)")
        self.rpe_entry.pack(pady=5)

        self.sleep_entry = ctk.CTkEntry(self, placeholder_text="Sleep (hours)")
        self.sleep_entry.pack(pady=5)

        self.soreness_entry = ctk.CTkEntry(self, placeholder_text="Soreness Level (1-5)")
        self.soreness_entry.pack(pady=5)

        self.status_label = ctk.CTkLabel(self, text="", text_color="tomato", wraplength=360, justify="left")
        self.status_label.pack(pady=5)

        self.submit_button = ctk.CTkButton(self, text="Submit Log", command=self.submit_log)
        self.submit_button.pack(pady=15)

    def _parse_athlete_id(self, raw: str, errors: list[str]) -> int | None:
        raw = raw.strip()
        if not raw:
            errors.append("Athlete ID is required.")
            return None
        try:
            athlete_id = int(raw)
        except ValueError:
            errors.append("Athlete ID must be a whole number.")
            return None
        if athlete_id <= 0:
            errors.append("Athlete ID must be a positive number.")
            return None
        return athlete_id

    def _parse_entry_date(self, raw: str, errors: list[str]) -> date | None:
        raw = raw.strip()
        if not raw:
            return date.today()
        try:
            parsed = datetime.strptime(raw, "%Y-%m-%d").date()
        except ValueError:
            errors.append("Date must be in YYYY-MM-DD format.")
            return None
        if parsed > date.today():
            errors.append("Date cannot be in the future.")
            return None
        return parsed

    def _parse_int_field(
        self, raw: str, label: str, min_value: int, max_value: int, errors: list[str]
    ) -> int | None:
        raw = raw.strip()
        if not raw:
            errors.append(f"{label} is required.")
            return None
        try:
            value = int(raw)
        except ValueError:
            errors.append(f"{label} must be a whole number.")
            return None
        if value < min_value or value > max_value:
            errors.append(f"{label} must be between {min_value} and {max_value}.")
            return None
        return value

    def _parse_float_field(
        self, raw: str, label: str, min_value: float, max_value: float, errors: list[str]
    ) -> float | None:
        raw = raw.strip()
        if not raw:
            errors.append(f"{label} is required.")
            return None
        try:
            value = float(raw)
        except ValueError:
            errors.append(f"{label} must be a number.")
            return None
        if value < min_value or value > max_value:
            errors.append(f"{label} must be between {min_value} and {max_value}.")
            return None
        return value

    def submit_log(self):
        errors: list[str] = []

        athlete_id = self._parse_athlete_id(self.athlete_id_entry.get(), errors)
        entry_date = self._parse_entry_date(self.entry_date_entry.get(), errors)
        duration_minutes = self._parse_int_field(
            self.duration_entry.get(), "Duration", MIN_DURATION_MINUTES, MAX_DURATION_MINUTES, errors
        )
        rpe = self._parse_int_field(self.rpe_entry.get(), "RPE", MIN_RPE, MAX_RPE, errors)
        sleep_hours = self._parse_float_field(
            self.sleep_entry.get(), "Sleep hours", MIN_SLEEP_HOURS, MAX_SLEEP_HOURS, errors
        )
        soreness_level = self._parse_int_field(
            self.soreness_entry.get(), "Soreness level", MIN_SORENESS, MAX_SORENESS, errors
        )

        if errors:
            self._show_error("\n".join(errors))
            return

        with get_session() as session:
            athlete = session.get(Athlete, athlete_id)
            if athlete is None:
                self._show_error(f"No athlete found with ID {athlete_id}.")
                return
            athlete_name = athlete.name

            log = DailyLog(
                athlete_id=athlete_id,
                entry_date=entry_date,
                duration_minutes=duration_minutes,
                rpe=rpe,
                sleep_hours=sleep_hours,
                soreness_level=soreness_level,
            )
            session.add(log)
            session.commit()

        self._show_success(f"Log saved for {athlete_name} on {entry_date.isoformat()}.")
        self._clear_fields()

    def _show_error(self, message: str):
        self.status_label.configure(text=message, text_color="tomato")

    def _show_success(self, message: str):
        self.status_label.configure(text=message, text_color="light green")

    def _clear_fields(self):
        for entry in (
            self.athlete_id_entry,
            self.entry_date_entry,
            self.duration_entry,
            self.rpe_entry,
            self.sleep_entry,
            self.soreness_entry,
        ):
            entry.delete(0, "end")
