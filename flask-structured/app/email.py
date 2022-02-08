from flask_mail import Message
from flask import current_app
from flask import render_template
from . import mail


def send_mail(to, subject, template, user, token):
    msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=current_app.config['FLASKY_MAIL_SENDER'],
                  recipients=[to])
    msg.body = render_template(template + '.txt', user=user, token=token)
    msg.html = render_template(template + '.html', user=user, token=token)
    mail.send(msg)
    return True
