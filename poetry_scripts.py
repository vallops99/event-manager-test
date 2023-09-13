import os
import sys
import dotenv

dotenv.load_dotenv()

def makemigrations():
    '''Run Django makemigrations command.'''
    stringed_args = ' '.join(sys.argv[1:])
    os.system(f'python manage.py makemigrations {stringed_args}')

def migrate():
    '''Run Django migrate command.'''
    stringed_args = ' '.join(sys.argv[1:])
    os.system(f'python manage.py migrate {stringed_args}')

def start_project():
    '''Run Django runserver command'''
    stringed_args = ' '.join(sys.argv[1:])
    os.system(f'gunicorn --bind 0.0.0.0:8000 event_manager_test.asgi -w 4 -k uvicorn.workers.UvicornWorker {stringed_args}')

def createsuperuser():
    '''Run Django createsuperuser command.'''
    stringed_args = ' '.join(sys.argv[1:])
    os.system(f'python manage.py createsuperuser {stringed_args}')

def pytest():
    '''Run pytest command.'''
    stringed_args = ' '.join(sys.argv[1:])
    os.system(f'pytest {stringed_args}')
