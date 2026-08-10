import customtkinter as ctk
from database.db_engine import get_session
from database.models import DailyLog
from analytics.risk_calc import eval_athlete_risk

# temporary ui for athlete view
class AthleteCheckInView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(self, text="Athlete Check-In", font=("Arial", 20, "bold"))
        self.label.pack(pady=10)

        self.athlete_id_entry = ctk.CTkEntry(self, placeholder_text="Enter Athlete ID")
        self.athlete_id_entry.pack(pady=5)

        self.duration_entry = ctk.CTkEntry(self, placeholder_text="Duration (minutes)")
        self.duration_entry.pack(pady=5)

        self.rpe_entry = ctk.CTkEntry(self, placeholder_text="RPE (1-10)")
        self.rpe_entry.pack(pady=5)

        self.sleep_entry = ctk.CTkEntry(self, placeholder_text="Sleep (hours)")
        self.sleep_entry.pack(pady=5)

        self.soreness_entry = ctk.CTkEntry(self, placeholder_text="Soreness Level (1-5)")
        self.soreness_entry.pack(pady=5)

        self.submit_button = ctk.CTkButton(self, text="Submit Log", command=self.submit_log)
        self.submit_button.pack(pady=15)

    def submit_log(self):
        print("Submit button clicked!")