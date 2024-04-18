import os
from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv())


workers = int(os.environ.get('GUNICORN_PROCESSES', '1'))

threads = int(os.environ.get('GUNICORN_THREADS', '1'))

timeout = int(os.environ.get('GUNICORN_TIMEOUT', '0'))

bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8080')

forwarded_allow_ips = '*'

secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }