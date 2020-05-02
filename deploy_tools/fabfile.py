import random
import string
import logging
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
        _configure_nginx()
        _configure_systemd_gunicorn()
        _load_services()
        
def _get_latest_source():
    logging.info(f'Get latest source from {REPO_URL}')
    if exists('.git'):
        run('git fetch')
    else:
        run(f'git clone {REPO_URL} .')
        
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'git reset --hard {current_commit}')
    
def _update_virtualenv():
    logging.info('Update virtual environment in venv')
    if not exists('venv/bin/pip'):
        run(f'python -m venv venv')
    run('./venv/bin/python -m pip install --upgrade pip')
    run('./venv/bin/pip install -r requirements.txt')
    
def _create_or_update_dotenv():
    logging.info('Updating .env file with appropriate variables')
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
    logging.info('Collecting static files')
    run('./venv/bin/python manage.py collectstatic --noinput')
    
    logging.info(f'Prividing static files at /srv/{env.host}/static')
    run(
        f'sudo mkdir -p /srv/{env.host}/'
        f' && sudo cp -r ./static /srv/{env.host}'
        f' && sudo chown -R :nginx /srv/{env.host}'
    )
    
def _update_database():
    logging.info('Updating database')
    run('./venv/bin/python manage.py migrate --noinput')
    
def _configure_nginx():
    logging.info('Configuring nginx config')
    run(
        f'cat ./deploy_tools/nginx.DOMAIN.template.conf'
        f'| sed "s/DOMAIN/{env.host}/g"'
        f'| sudo tee /etc/nginx/conf.d/{env.host}.conf'
    )
    
def _configure_systemd_gunicorn():
    logging.info('Configuring gunicorn systemd service')
    run(
        f'cat ./deploy_tools/gunicorn-systemd.template.service'
        f'| sed "s/DOMAIN/{env.host}/g"'
        f'| sudo tee /etc/systemd/system/gunicorn-{env.host}.service'
    )
    
def _load_services():
    logging.info('Starting and enabling services')
    run(
        f'sudo systemctl daemon-reload'
        f' && sudo systemctl reload nginx'
        f' && sudo systemctl enable gunicorn-{env.host}.service'
        f' && sudo systemctl start gunicorn-{env.host}.service'
    )
