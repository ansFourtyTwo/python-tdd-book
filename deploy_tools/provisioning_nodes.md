Provisioning a new site
=======================

## Required packages:

 * nginx
 * Python 3.7+
 * virtualenv + pip
 * git

## NGINX Virtual host config

 * see nginx.template.conf and nginx.DOMAIN.template.conf
 * replace DOMAIN with the actual domain, e.g. staging.funkers.de

## Systemd service

 * see gunicorn-systemd.template.service
 * replace DOMAIN with the actual domain, e.g. staging.funkers.de

 e.g. on Fedora:
	sed -i 's/DOMAIN/staging.funkers.de/g' gunicorn-systemd.template.service

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

