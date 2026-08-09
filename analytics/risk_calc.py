import pandas as pd
from sqlmodel import select
from database.db_engine import get_session
from database.models import DailyLog

def get_athlete_df(athlete_id: int) -> pd.DataFrame:
    with get_session() as session:
        statement = select(DailyLog).where(DailyLog.athlete_id == athlete_id).order_by(DailyLog.entry_date)
        results = session.exec(statement).all()

        data = [log.model_dump() for log in results]
        if not data:
            return pd.DataFrame() 
        return pd.DataFrame(data)

def eval_athlete_risk(athlete_id: int, df_override: pd.DataFrame = None) -> dict:
    if df_override is not None:
        df = df_override
    else:
        df = get_athlete_df(athlete_id)

    # ensure 7 days of data
    if len(df) < 7:
        return {"status": "INSUFFICIENT_DATA", "alerts": []}

    df['daily_workload'] = df['duration_minutes'] * df['rpe']
    
    # 7 day acute vs 28 day chronic load
    df['acute_load'] = df['daily_workload'].rolling(window=7, min_periods=3).mean()
    df['chronic_load'] = df['daily_workload'].rolling(window=28, min_periods=7).mean()
    df['acwr'] = df['acute_load'] / (df['chronic_load'] + 1e-5) 

    latest = df.iloc[-1]
    alerts = []
    status = "GREEN"

    # high acwr spikes > 1.5
    if latest['acwr'] > 1.5:
        alerts.append(f"CRITICAL: ACWR spike to {latest['acwr']:.2f} (High Injury Risk)")
        status = "RED"
    elif latest['acwr'] > 1.3:
        alerts.append(f"WARNING: ACWR elevated to {latest['acwr']:.2f}")
        if status != "RED": status = "YELLOW"

    # chronic sleep depr + high soreness
    if latest['sleep_hours'] < 6.5 and latest['soreness_level'] >= 4:
        alerts.append(f"WARNING: Sleep deprivation ({latest['sleep_hours']} hrs) + High Soreness ({latest['soreness_level']})")
        if status != "RED": status = "YELLOW"

    return {
        "athlete_id": athlete_id,
        "status": status,
        "acwr": round(latest['acwr'], 2),
        "alerts": alerts    
    }