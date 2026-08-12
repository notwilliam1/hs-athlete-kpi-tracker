import re

import customtkinter as ctk

from database.db_engine import get_session
from database.models import Athlete

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
MAX_NAME_LENGTH = 100
MAX_SPORT_LENGTH = 50


class AddAthleteView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.header = ctk.CTkLabel(self, text="Add New Athlete", font=("Arial", 20, "bold"))
        self.header.pack(pady=(10, 0))

        self.athlete_name_entry = ctk.CTkEntry(self, placeholder_text="Athlete Name")
        self.athlete_name_entry.pack(pady=5)

        self.athlete_sport_entry = ctk.CTkEntry(self, placeholder_text="Athlete Sport")
        self.athlete_sport_entry.pack(pady=5)

        self.athlete_coach_email_entry = ctk.CTkEntry(self, placeholder_text="Coach Email")
        self.athlete_coach_email_entry.pack(pady=5)

        self.athlete_pt_email_entry = ctk.CTkEntry(self, placeholder_text="PT Email (optional)")
        self.athlete_pt_email_entry.pack(pady=5)

        self.status_label = ctk.CTkLabel(self, text="", text_color="tomato", wraplength=360, justify="left")
        self.status_label.pack(pady=5)

        self.submit_button = ctk.CTkButton(self, text="Add Athlete", command=self.submit_athlete)
        self.submit_button.pack(pady=15)

    def _parse_required_text(self, raw: str, label: str, max_length: int, errors: list[str]) -> str | None:
        value = raw.strip()
        if not value:
            errors.append(f"{label} is required.")
            return None
        if len(value) > max_length:
            errors.append(f"{label} must be {max_length} characters or fewer.")
            return None
        return value

    def _parse_required_email(self, raw: str, label: str, errors: list[str]) -> str | None:
        value = raw.strip()
        if not value:
            errors.append(f"{label} is required.")
            return None
        if not EMAIL_PATTERN.match(value):
            errors.append(f"{label} must be a valid email address.")
            return None
        return value

    def _parse_optional_email(self, raw: str, label: str, errors: list[str]) -> str | None:
        value = raw.strip()
        if not value:
            return None
        if not EMAIL_PATTERN.match(value):
            errors.append(f"{label} must be a valid email address.")
            return None
        return value

    def submit_athlete(self):
        errors: list[str] = []

        name = self._parse_required_text(self.athlete_name_entry.get(), "Athlete name", MAX_NAME_LENGTH, errors)
        sport = self._parse_required_text(self.athlete_sport_entry.get(), "Sport", MAX_SPORT_LENGTH, errors)
        coach_email = self._parse_required_email(self.athlete_coach_email_entry.get(), "Coach email", errors)
        pt_email = self._parse_optional_email(self.athlete_pt_email_entry.get(), "PT email", errors)

        if errors:
            self._show_error("\n".join(errors))
            return

        with get_session() as session:
            athlete = Athlete(
                name=name,
                sport=sport,
                coach_email=coach_email,
                pt_email=pt_email,
            )
            session.add(athlete)
            session.commit()
            session.refresh(athlete)
            athlete_id = athlete.id

        self._show_success(f"Added {name} (ID {athlete_id}). Use this ID in Check-In.")
        self._clear_fields()

    def _show_error(self, message: str):
        self.status_label.configure(text=message, text_color="tomato")

    def _show_success(self, message: str):
        self.status_label.configure(text=message, text_color="light green")

    def _clear_fields(self):
        for entry in (
            self.athlete_name_entry,
            self.athlete_sport_entry,
            self.athlete_coach_email_entry,
            self.athlete_pt_email_entry,
        ):
            entry.delete(0, "end")
