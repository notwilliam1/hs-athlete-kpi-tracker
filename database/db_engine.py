from typing import Optional
from datetime import date
from sqlmodel import SQLModel, Field, Relationship

class Athlete(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    sport: str
    coach_email: str
    pt_email: Optional[str] = None