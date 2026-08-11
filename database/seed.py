from datetime import date, timedelta

from sqlmodel import Session, select

from database.db_engine import get_session
from database.models import Athlete, DailyLog

# (days, duration_minutes, rpe, sleep_hours, soreness_level) segments, oldest first.
SAMPLE_ATHLETES = [
    {
        "name": "Jordan Lee",
        "sport": "Track & Field",
        "coach_email": "coach.jordan@example.com",
        "segments": [(30, 60, 5, 8.0, 2)],  # GREEN: steady load, ACWR ~ 1.0
    },
    {
        "name": "Morgan Reyes",
        "sport": "Soccer",
        "coach_email": "coach.morgan@example.com",
        "pt_email": "pt.morgan@example.com",
        "segments": [
            (21, 30, 3, 8.0, 2),
            (7, 120, 9, 7.0, 3),
        ],  # RED: 7-day load spike pushes ACWR > 1.5
    },
    {
        "name": "Casey Kim",
        "sport": "Basketball",
        "coach_email": "coach.casey@example.com",
        "segments": [(30, 60, 5, 5.5, 4)],  # YELLOW: steady load, low sleep + high soreness
    },
    {
        "name": "Riley Chen",
        "sport": "Swimming",
        "coach_email": "coach.riley@example.com",
        "segments": [(5, 45, 4, 7.5, 2)],  # INSUFFICIENT_DATA: only 5 logs
    },
]


def _dates_for(days: int) -> list[date]:
    today = date.today()
    return [today - timedelta(days=(days - 1 - i)) for i in range(days)]


def _logs_from_segments(athlete_id: int, segments: list[tuple[int, int, int, float, int]]) -> list[DailyLog]:
    total_days = sum(segment[0] for segment in segments)
    dates = iter(_dates_for(total_days))

    logs = []
    for days, duration_minutes, rpe, sleep_hours, soreness_level in segments:
        for _ in range(days):
            logs.append(
                DailyLog(
                    athlete_id=athlete_id,
                    entry_date=next(dates),
                    duration_minutes=duration_minutes,
                    rpe=rpe,
                    sleep_hours=sleep_hours,
                    soreness_level=soreness_level,
                )
            )
    return logs


def seed_sample_data(session: Session | None = None) -> list[Athlete]:
    owns_session = session is None
    session = session or get_session()
    if owns_session:
        # keep returned Athlete objects usable after this function closes the session
        session.expire_on_commit = False

    try:
        if session.exec(select(Athlete)).first() is not None:
            return []

        seeded = []
        for entry in SAMPLE_ATHLETES:
            athlete = Athlete(
                name=entry["name"],
                sport=entry["sport"],
                coach_email=entry["coach_email"],
                pt_email=entry.get("pt_email"),
            )
            session.add(athlete)
            session.commit()
            session.refresh(athlete)

            for log in _logs_from_segments(athlete.id, entry["segments"]):
                session.add(log)
            session.commit()

            seeded.append(athlete)

        return seeded
    finally:
        if owns_session:
            session.close()
