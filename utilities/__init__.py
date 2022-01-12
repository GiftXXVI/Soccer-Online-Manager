import smtplib
from email.message import EmailMessage
from datetime import datetime


def sendmail(recepient, message):
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = f'Please confirm your email address.'
    msg['From'] = 'no-reply@soccermanager.local'
    msg['To'] = recepient
    s = smtplib.SMTP(host='localhost', port=8025)
    s.send_message(msg)
    s.quit()
