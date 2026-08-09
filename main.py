import customtkinter as ctk
from ui.athlete_view import AthleteCheckInView

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class AppUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Athlete KPI Tracker & Risk Assessment")
        self.geometry("800x600")

        # tab view nav
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(padx=20, pady=20, fill="both", expand=True)

        self.tab_athlete = self.tabview.add("Athlete Check-In")
        self.tab_coach = self.tabview.add("Coach Dashboard")

        self.athlete_view = AthleteCheckInView(self.tab_athlete)
        self.athlete_view.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = AppUI()
    app.mainloop()