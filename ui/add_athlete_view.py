import customtkinter as ctk

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

        self.submit_button = ctk.CTkButton(self, text="Add Athlete", command=self.submit_athlete)
        self.submit_button.pack(pady=15)

    def submit_athlete(self):
        print("Submit athlete functionality not implemented yet.")