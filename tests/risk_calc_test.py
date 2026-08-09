import pytest
import pandas as pd
from analytics.risk_calc import eval_athlete_risk

def sample_logs(days: int, rpe: int, duration_minutes: int, sleep_hours: float, soreness_level: int) -> pd.DataFrame:
    dates = pd.date_range(end=pd.Timestamp.today(), periods=days)
    data = {
        "entry_date": dates,
        "rpe": [rpe] * days,
        "duration_minutes": [duration_minutes] * days,
        "sleep_hours": [sleep_hours] * days,
        "soreness_level": [soreness_level] * days,
    }
    return pd.DataFrame(data)

def test_insufficient_data():
    df_short = sample_logs(days=5, rpe=5, duration_minutes=60, sleep_hours=8.0, soreness_level=2)

    result = eval_athlete_risk(athlete_id=1, df_override=df_short)

    assert result["status"] == "INSUFFICIENT_DATA"
    assert len(result["alerts"]) == 0

# steady workload over 28 days should result in GREEN status
def test_baseline_green_status():
    df_steady = sample_logs(days=28, rpe=5, duration_minutes=60, sleep_hours=8.0, soreness_level=2)

    result = eval_athlete_risk(athlete_id=1, df_override=df_steady)

    assert result["status"] == "GREEN"
    assert result["acwr"] < 1.05
    assert len(result["alerts"]) == 0

# sudden 3x spike in workload in past 7 days should trigger RED status
def test_acwr_spike_red_status():
    # 21 days of low workload
    df_baseline = sample_logs(days=21, rpe=3, duration_minutes=30, sleep_hours=8.0, soreness_level=2)

    # 7 days of high workload
    df_spike = sample_logs(days=7, rpe=9, duration_minutes=120, sleep_hours=8.0, soreness_level=2)

    df_combined = pd.concat([df_baseline, df_spike], ignore_index=True)

    result = eval_athlete_risk(athlete_id=1, df_override=df_combined)

    assert result["status"] == "RED"
    assert result["acwr"] > 1.5
    assert any("CRITICAL" in alert for alert in result["alerts"])

# normal acr but low sleep and high soreness should trigger YELLOW status
def test_sleep_and_soreness_yellow():
    df_logs = sample_logs(days=28, rpe=5, duration_minutes=60, sleep_hours=5.5, soreness_level=4)

    result = eval_athlete_risk(athlete_id=1, df_override=df_logs)

    assert result["status"] == "YELLOW"
    assert any("Soreness" in alert for alert in result["alerts"])