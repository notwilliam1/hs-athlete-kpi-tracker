from datetime import date

from database.db_engine import get_session
from database.db_engine import init_db
from database.models import Athlete
from database.models import DailyLog
from sqlmodel import select

def test_db():
    init_db()

    with get_session() as session:
        dummy_athlete = Athlete(name="John Doe", sport="football", coach_email="john.doe@example.com")

        session.add(dummy_athlete)
        session.commit()
        session.refresh(dummy_athlete)

        saved_dummy_athlete_id = dummy_athlete.id

        log = DailyLog(
            athlete_id = dummy_athlete.id,
            entry_date = date.today(),
            duration_minutes = 60,
            rpe = 7,
            sleep_hours = 8.0,
            soreness_level = 3            
        )
        session.add(log)
        session.commit()

    with get_session() as session:
        statement = select(DailyLog).where(DailyLog.athlete_id == saved_dummy_athlete_id)
        saved_log = session.exec(statement).first()

        if saved_log:
            print(f"Athelete: {saved_log.athlete.name}, Sport: {saved_log.athlete.sport}, Coach Email: {saved_log.athlete.coach_email}")
            print(f"Log Date: {saved_log.entry_date}, Duration: {saved_log.duration_minutes} minutes, RPE: {saved_log.rpe}, Sleep Hours: {saved_log.sleep_hours}, Soreness Level: {saved_log.soreness_level}")
        else:
            print("No log found for the athlete.")

if __name__ == "__main__":
    test_db()