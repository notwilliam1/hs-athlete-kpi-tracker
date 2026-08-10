from unittest.mock import patch, MagicMock
import pytest
from notifications.alert_service import send_alert_email

@pytest.fixture
def red_risk_report():
    return {
        "status": "RED",
        "acwr": 1.68,
        "alerts": [
            "ACWR is 1.68 (Above 1.65 high-risk threshold)",
            "High soreness rating: 4/5",
            "Low sleep duration: 4.5 hours"
        ]
    }

@pytest.fixture
def green_risk_report():
    return {
        "status": "GREEN",
        "acwr": 1.05,
        "alerts": []
    }

def test_send_alert_email_ignores_green(green_risk_report):
    with patch("notifications.alert_service.smtplib.SMTP_SSL") as mock_smtp:
        result = send_alert_email(recipient_email="test@example.com", athlete_name="John Doe", alerts=green_risk_report["alerts"])
        
        assert result is False or result is None
        mock_smtp.assert_not_called()

@patch("notifications.alert_service.smtplib.SMTP_SSL")
def test_send_alert_email_red_status(mock_smtp_class, red_risk_report):
    mock_smtp_instance = MagicMock()
    mock_smtp_class.return_value.__enter__.return_value = mock_smtp_instance

    result = send_alert_email(recipient_email="test@example.com", athlete_name="John Doe", alerts=red_risk_report["alerts"])

    mock_smtp_class.assert_called_once()

    assert mock_smtp_instance.sendmail.called or mock_smtp_instance.send_message.called

@patch("notifications.alert_service.smtplib.SMTP_SSL")
def test_send_alert_email_handles_smtp_error(mock_smtp_class, red_risk_report):
    mock_smtp_class.side_effect = Exception("SMTP Connection Refused")

    try:
        result = send_alert_email(recipient_email="test@example.com", athlete_name="John Doe", alerts=red_risk_report["alerts"])
        assert result is False or result is None
    except Exception as e:
        pytest.fail(f"send_alert_email raised an uncaught exception: {e}")