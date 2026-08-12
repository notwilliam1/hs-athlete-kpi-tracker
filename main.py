import customtkinter as ctk
from ui.athlete_view import AthleteCheckInView
from ui.coach_view import CoachDashboardView
from ui.add_athlete_view import AddAthleteView
from database.db_engine import init_db
from database.seed import seed_sample_data

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

init_db()
seeded = seed_sample_data()
if seeded:
    print("Seeded sample athletes (use these IDs in Check-In):")
    for athlete in seeded:
        print(f"  {athlete.id}: {athlete.name} ({athlete.sport})")

class AppUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Athlete KPI Tracker & Risk Assessment")
        self.geometry("1200x600")

        # tab view nav
        self.tabview = ctk.CTkTabview(self, command=self._on_tab_change)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        self.tab_athlete = self.tabview.add("Athlete Check-In")
        self.tab_coach = self.tabview.add("Coach Dashboard")
        self.tab_add_athlete = self.tabview.add("Add Athlete")

        self.athlete_view = AthleteCheckInView(self.tab_athlete)
        self.athlete_view.pack(fill="both", expand=True)

        self.coach_view = CoachDashboardView(self.tab_coach)
        self.coach_view.pack(fill="both", expand=True)

        self.add_athlete = AddAthleteView(self.tab_add_athlete)
        self.add_athlete.pack(fill="both", expand=True)

    def _on_tab_change(self):
        if self.tabview.get() == "Coach Dashboard":
            self.coach_view.refresh()

if __name__ == "__main__":
    app = AppUI()
    app.mainloop()