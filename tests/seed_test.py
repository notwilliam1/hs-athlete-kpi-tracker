import pytest

from sqlmodel import SQLModel, Session, create_engine, select

from database.models import Athlete, DailyLog
from database.seed import seed_sample_data


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_seed_creates_athletes_and_logs(session):
    seeded = seed_sample_data(session)

    assert len(seeded) == 4
    assert len(session.exec(select(Athlete)).all()) == 4
    assert len(session.exec(select(DailyLog)).all()) == 30 + 28 + 30 + 5


def test_seed_is_idempotent(session):
    seed_sample_data(session)
    second_pass = seed_sample_data(session)

    assert second_pass == []
    assert len(session.exec(select(Athlete)).all()) == 4
    assert len(session.exec(select(DailyLog)).all()) == 30 + 28 + 30 + 5
