from decouple import config

DB_USER = config('DB_USER')
DB_PASS = config('DB_PASS')
DB_HOST = config('DB_HOST')
DB_PORT = config('DB_PORT')
DB_NAME = config('DB_NAME')


SMTP_USER = config("SMTP_USER")
SMTP_PASSWORD = config("SMTP_PASSWORD")