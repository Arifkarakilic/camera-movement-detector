import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()

def send_alert_email():
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    msg = EmailMessage()
    msg["Subject"] = "Kamera hareket algıladı!"
    msg["From"] = smtp_user
    msg["To"] = receiver_email
    msg.set_content("Kamera hareket algıladı. Lütfen kontrol edin.")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(smtp_user, smtp_pass)
            smtp.send_message(msg)
        print("Email başarıyla gönderildi.")
        return True
    except Exception as e:
        print(f"Email gönderilemedi: {e}")
        return False