import pytest
from datetime import date

from sqlmodel import SQLModel, Session, create_engine

from database.models import Athlete, DailyLog


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_create_athlete(session):
    athlete = Athlete(
        name="John Pork",
        sport="Football",
        coach_email="john.pork@example.com",
    )
    session.add(athlete)
    session.commit()
    session.refresh(athlete)

    assert athlete.id is not None
    assert athlete.pt_email is None


def test_create_daily_log(session):
    athlete = Athlete(
        name="Jane Pig",
        sport="Soccer",
        coach_email="jane.pig@example.com",
    )
    session.add(athlete)
    session.commit()
    session.refresh(athlete)

    log = DailyLog(
        athlete_id=athlete.id,
        entry_date=date.today(),
        duration_minutes=60,
        rpe=7,
        sleep_hours=8.0,
        soreness_level=3,
    )
    session.add(log)
    session.commit()
    session.refresh(log)

    assert log.id is not None
    assert log.rpe == 7
    assert log.soreness_level == 3


def test_relationship_loads_athlete(session):
    athlete = Athlete(
        name="Alex Smith",
        sport="Basketball",
        coach_email="alex.smith@example.com",
    )
    session.add(athlete)
    session.commit()
    session.refresh(athlete)

    log = DailyLog(
        athlete_id=athlete.id,
        entry_date=date.today(),
        duration_minutes=45,
        rpe=6,
        sleep_hours=7.5,
        soreness_level=2,
    )
    session.add(log)
    session.commit()
    session.refresh(log)

    assert log.athlete.name == "Alex Smith"
    assert log.athlete.sport == "Basketball"
    assert athlete.logs[0].id == log.id