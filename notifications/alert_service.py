import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_alert_email(recipient_email: str, athlete_name: str, alerts: list[str]):
    if not alerts:
        return

    body = f"High Risk Flagged for {athlete_name}:\n\n" + "\n".join([f"- {a}" for a in alerts])
    msg = MIMEText(body)
    msg['Subject'] = f"High Risk Alert: {athlete_name}"
    msg['From'] = os.getenv("SENDER_EMAIL")
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP_SSL(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT", 465))) as server:
            server.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
            server.sendmail(os.getenv("SENDER_EMAIL"), [recipient_email], msg.as_string())
        print(f"Alert successfully sent to {recipient_email}")
    except Exception as e:
        print(f"Failed to send alert email: {e}")