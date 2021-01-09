import requests
import os
import smtplib

if requests.get('http://localhost').status_code != 200:
    gmail_user = os.getenv("GMAIL_USERNAME")
    gmail_password = os.getenv("GMAIL_PASS")

    sent_from = gmail_user
    to = ['me@gmail.com', 'test@gmail.com']
    subject = 'Application is not working'
    body = 'Server application is not working, please check!'

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print('Email sent!')
    except:
        print('Email could not be sent')
