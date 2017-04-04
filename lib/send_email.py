# -*- coding:utf-8 -*-
import smtplib
from config.default_celery import celery_app


@celery_app.task(name='send_error_email')
def send_error_email(host, port, fromaddr, toaddrs, subject, username=None,
               password=None, time=5, msg='', secure=None):
    """
    """
    if not port:
        port = smtplib.SMTP_PORT

    smtp = smtplib.SMTP(host, port, timeout=time)

    if username:
        if secure:
            smtp.ehlo()
            smtp.starttls(*secure)
            smtp.ehlo()
        smtp.login(username, password)
    smtp.sendmail(fromaddr, toaddrs, msg)

    smtp.quit()
