import redis
import json 
import os
import smtplib
from email.mime.text import MIMEText

if __name__ == '__main__':
    redis_host = os.getenv('REDIS_HOST')
    r = redis.Redis(host=redis_host, port=6379, db=0)
    print('---------- READY AND WAITING FOR MESSAGES ---------- ')
    while True:
        messageForm = json.loads(r.blpop('sender')[1])

        print('Preparing message to be sent: ', messageForm['subject'])

        sender = 'admin@example.com'
        receiver = 'info@example.com'

        msg = MIMEText(messageForm['message'])

        msg['Subject'] = 'Hello ✔'
        msg['From'] = sender
        msg['To'] = receiver

        user = os.getenv('SMTP_USER') 
        password = os.getenv('SMTP_PASSWORD')

        server = smtplib.SMTP('smtp.mailtrap.io', 2525)
        server.starttls()
        server.login(user, password)
        server.sendmail(sender, receiver, msg.as_string())

        print('Message', messageForm['subject'], 'sent')