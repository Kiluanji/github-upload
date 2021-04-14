#!/usr/bin/env python3

import email, smtplib, ssl, os

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def email_results(
        subject="An email with attachment from Python",
        body="This is an email with attachment sent from Python",
        sender_email="alvaroneto.ch@gmail.com",
        receiver_email="alvaroneto.ch@gmail.com",
        files=[]
        ):

    #subject = "An email with attachment from Python"
    #body = "This is an email with attachment sent from Python"
    #sender_email = "alvaroneto.ch@gmail.com"
    #receiver_email = "alvaroneto.ch@gmail.com"
    with open('/home/alvaro/gmail_password.txt') as f:
        password = f.read().rstrip('\n')

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    for x in files:
        attachment = open(x, 'rb')
        filename = os.path.basename(x)
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        part.add_header('Content-Disposition', 'attachment', filename=filename)
        encoders.encode_base64(part)
        message.attach(part)

    text = message.as_string()

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
