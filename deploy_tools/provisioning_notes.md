Provisioning a new site
=======================

## Required packages:

 * nginx
 * Python 3.7+
 * virtualenv + pip
 * git
 * certbot, certbot-nginx
 
## NGINX Virtual host config

 * see nginx.template.conf and nginx.DOMAIN.template.conf
 * replace DOMAIN with the actual domain, e.g. staging.funkers.de

## Systemd service

 * see gunicorn-systemd.template.service
 * replace DOMAIN with the actual domain, e.g. staging.funkers.de

 e.g. on Fedora:
	`sed -i 's/DOMAIN/staging.funkers.de/g' gunicorn-systemd.template.service`

## HTTPS encryption (SSL with Let's encrpyt)

 * Install certbot and certbot-nginx: `sudo dnf install certbot certbot-nginx`
 * Run certbot and follow instructions: `sudo certbot -nginx`
 * Install cronjob to frequently update expiring certificates: 
 ```
 echo "0 0,12 * * * root python -c 'import random; import time; time.sleep(random.random() * 3600)' && certbot renew -q" | sudo tee -a /etc/crontab > /dev/null
 ```

## Folder structure

/home/sfink
└── sites
    └── DOMAIN1
        ├── db.sqlite3
        ├── deploy_tools
        ├── functional_tests
        ├── lists
        ├── manage.py
        ├── requirements.txt
        ├── static
        ├── superlist
        └── venv

