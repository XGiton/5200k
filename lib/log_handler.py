# -*- coding: utf-8 -*-
"""
Define different log handler here
"""
from cache import r
from config import (
    EMAIL_HOST,
    EMAIL_ADDR,
    EMAIL_SUBJECT,
    EMAIL_PWD,
    ADMINS,
    LOG_REPEAT_TIMES,
    LOG_INTERVAL_TIME,
)
from config.default_celery import celery_app
from logging import Handler, Filter, Formatter, WARNING, ERROR, INFO
from logging.handlers import SMTPHandler, HTTPHandler


class LogFrequencyFilter(Filter):
    """: Filter for log frequency
    """
    def __init__(self, name=''):
        Filter.__init__(self, name=name)

    def filter(self, record):
        """: Filter if the curtom log
        """
        if super(LogFrequencyFilter, self).filter(record) == 0:
            return 0

        # distinuguish this error log
        key = ','.join((
            record.module,
            record.filename,
            record.funcName,
            str(record.lineno),
            record.levelname
        ))

        # get redis value of this key
        v = r.incr(key)

        if v <= LOG_REPEAT_TIMES:
            # check if need set expire time
            if v == 1:
                # set expire
                r.expire(key, LOG_INTERVAL_TIME)
            # will be handled
            return 1
        else:
            return 0


class CustomSMTPHandler(SMTPHandler):
    """: Email to admins if occurs errors
    """
    def __init__(self, mailhost, fromaddr, toaddrs, subject,
                 credentials=None, secure=None):
        SMTPHandler.__init__(self, mailhost, fromaddr, toaddrs, subject,
                             credentials, secure)

    def emit(self, record):
        """
        Override handler for sending async error emails
        """
        from email.utils import formatdate
        msg = self.format(record)
        msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
            self.fromaddr,
            ",".join(self.toaddrs),
            self.getSubject(record),
            formatdate(),
            msg)
        celery_app.send_task(
            'send_error_email',
            (
                self.mailhost,
                self.mailport,
                self.fromaddr,
                self.toaddrs,
                self.subject,
            ),
            {
                'username': self.username,
                'password': self.password,
                'msg': msg,
                'secure': self.secure,
            },
        )


# create a smtp handler
mailer = CustomSMTPHandler(EMAIL_HOST,
                           EMAIL_ADDR,
                           ADMINS,
                           EMAIL_SUBJECT,
                           (EMAIL_ADDR, EMAIL_PWD))
mailer.setFormatter(Formatter(
    '''
    Message type:    %(levelname)s
    Location:        %(pathname)s:%(lineno)d
    Module:          %(module)s
    Function:        %(funcName)s
    Time:            %(asctime)s
    Message:         %(message)s
    '''
))
mailer.addFilter(LogFrequencyFilter())
mailer.setLevel(WARNING)
