from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class Athlete(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    sport: str
    coach_email: str
    pt_email: Optional[str] = None

    logs: list["DailyLog"] = Relationship(back_populates="athlete")

class DailyLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    athlete_id: int = Field(foreign_key="athlete.id")
    entry_date: date

    duration_minutes: int
    rpe: int #scale 1-10 for rate of percieved exertion
    sleep_hours: float
    soreness_level: int #scale 1-5 for muscle soreness

    athlete: Optional[Athlete] = Relationship(back_populates="logs")