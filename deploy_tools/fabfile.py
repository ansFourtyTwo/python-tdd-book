import random
import string
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run

REPO_URL = 'https://github.com/ansFourtyTwo/python-tdd-book.git'

def deploy():
    print(f'Deploying host={env.host} for user={env.user}')
    site_folder = f'/home/{env.user}/sites/{env.host}'
    run(f'mkdir -p {site_folder}')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()
        
def _get_latest_source():
    print(f'Get latest source from {REPO_URL}')
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
        
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'git reset --hard {current_commit}')
    
def _update_virtualenv():
    print('Update virtual environment in venv')
    if not exists('venv/bin/pip'):
        run(f'python -m venv venv')
    run('./venv/bin/pip install -r requirements.txt')
    
def _create_or_update_dotenv():
    print('Updating .env file with appropriate variables')
    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    current_content = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_content:
        secret_key_symbols = (
            string.ascii_lowercase + 
            string.ascii_uppercase + 
            '0123456789' + 
            '!"§$%&'
        )
        new_secret = ''.join(random.SystemRandom().choices(
            secret_key_symbols, k=50
        ))
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')
        
def _update_static_files():
    print('Collecting static files')
    run('./venv/bin/python manage.py collectstatic --noinput')
    
def _update_database():
    print('Updating database')
    run('./venv/bin/python manage.py migrate --noinput')
