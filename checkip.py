from os.path import isfile
import time
import os
import requests
import subprocess
import smtplib, ssl
from email.message import EmailMessage


def get_ip_address():
    url = "https://api.ipify.org"
    response = requests.get(url, timeout=10)
    ip_add = response.text
    return ip_add


def check_internet_connection():
    try:
        subprocess.check_output(["ping", "-c", "1", "8.8.8.8"])
        return True
    except subprocess.CalledProcessError:
        return False


def send_email(id_address: str) -> None:
    email_sender = os.environ.get("EMAIL_SENDER")
    email_password = os.environ.get("EMAIL_PASSWORD")
    email_receiver = os.environ.get("EMAIL_RECEIVER")

    subject = "New ip address"
    body = "New ip address:+\n" + id_address
    email = EmailMessage()
    email["From"] = email_sender
    email["To"] = email_receiver
    email["Subject"] = subject
    email.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, email.as_string())


if __name__ == "__main__":
    if not os.path.isfile("ip_address.txt"):
        with open("ip_address.txt", "w", encoding="utf-8") as file:
            file.write("")
    while True:
        if get_ip_address():
            with open("./ip_address.txt", "r", encoding="utf-8") as file:
                pre_id_address = file.readline()
            curr_ip_address = get_ip_address()
            if pre_id_address.strip() != curr_ip_address:
                send_email(curr_ip_address)
                with open("./ip_address.txt", "w", encoding="utf-8") as file:
                    file.write(curr_ip_address)
            time.sleep(60)
        else:
            time.sleep(60)
