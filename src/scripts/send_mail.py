"""
Script to configurate an SMTP system to deliver and email with and attached 
image (jpg) located in the directory named "img".

A .env file is required with the following fields:

- SMTP_SERVER: the server to deliver the email (ex. "smtp.gmail.com")
- SENDER_EMAIL: "sender@email.com"
- RECEIVER_EMAIL: "receiver@email.com"
- PORT: the indicated port by the smtp server
- PASS: the password to grant access to the smtp server

"""
from email.message import EmailMessage
import smtplib, ssl
from dotenv import dotenv_values


config = dotenv_values(".env")

message = EmailMessage()
message['Subject'] = "Plantitas"
message['From'] = config["SENDER_EMAIL"]
message['To'] = config["RECEIVER_EMAIL"]
msg_content = """
AMO, este mensaje es para confirmar que sus entes verdes han sido humectados.
Cambio y fuera.
La RPi  ^.^ 
"""
message.set_content(msg_content)
with open("/RPirrigo/img/22_Aug_2022_00-38-52.jpg", "rb") as image_file:
    message.add_attachment(image_file.read(), maintype="image", subtype="jpg")

with smtplib.SMTP(config["SMTP_SERVER"], config["PORT"]) as server:
    context = ssl.create_default_context()
    server.starttls(context=context)
    server.login(config["SENDER_EMAIL"], config["PASS"])
    server.send_message(message)
print("Message sent")
