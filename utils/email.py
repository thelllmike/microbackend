import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Function to send an OTP via email
def send_otp_email(receiver_email: str, otp: str):
    sender_email = os.getenv("SENDER_EMAIL")  # Replace with your actual email
    sender_password = os.getenv("SENDER_PASSWORD")  # Replace with your email account password

    # Email content
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your OTP Code"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Email body
    text = f"Your OTP code is: {otp}"
    html = f"""
    <html>
    <body>
        <p>Your OTP code is:</p>
        <h2>{otp}</h2>
    </body>
    </html>
    """
    
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    # Send the email using SMTP
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("OTP email sent successfully!")
    except Exception as e:
        print(f"Failed to send OTP email: {e}")

# Function to send a password reset email
def send_reset_email(receiver_email: str, token: str):
    sender_email = os.getenv("SENDER_EMAIL")  # Replace with your actual email
    sender_password = os.getenv("SENDER_PASSWORD")  # Replace with your email account password

    # Email content
    message = MIMEMultipart("alternative")
    message["Subject"] = "Password Reset Request"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Email body
    text = f"Click the following link to reset your password: "
    html = f"""
    <html>
    <body>
        <p>Click the following link to reset your password:</p>
        <a href="http://127.0.0.1:8000/reset-password?token={token}">Reset Password</a>
    </body>
    </html>
    """
    
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    # Send the email using SMTP
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Password reset email sent successfully!")
    except Exception as e:
        print(f"Failed to send password reset email: {e}")