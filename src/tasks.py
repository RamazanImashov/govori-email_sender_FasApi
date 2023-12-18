import smtplib
from email.message import EmailMessage

from celery import Celery

from src.env_files import SMTP_PASSWORD, SMTP_USER

from decouple import config

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587

celery = Celery('tasks', broker='redis://localhost:6379')


smtplib.SMTP_TIMEOUT = 30


def get_email(types: str, price: float, name_type: str, username: str, emails: str, phone_number: str):
    email = EmailMessage()
    email['Subject'] = 'New client'
    email['From'] = config('EMAIL_HOST_USER')
    email['To'] = config('EMAIL_HOST_USER')

    email.set_content(
        '<!DOCTYPE html>'
        '<html lang="en">'
        '<head>'
        '<meta charset="UTF-8">'
        '<title>Title</title>'
        '</head>'
        '<body>'
        '<div class="card">'
        '<div class="card-body">'
        '<p class="text-center">'
        f'types: {types},<br>'
        f'price: {price},<br>'
        f'name_type: {name_type},<br>'
        f'username: {username},<br>'
        f'email: {emails},<br>'
        f'phone_number: {phone_number}<br>'
        '</p>'
        '</div>'
        '</div>'
        '</body>'
        '</html>',
        subtype='html'
    )
    return email


def send_email_bg(types: str, price: float, name_type: str, username: str, phone_number: str, emails: str):
    email = get_email(types, price, name_type, username, emails, phone_number)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)


celery.autodiscover_tasks()

