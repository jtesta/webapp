#!/bin/bash


echo -e "Creating webapp user...\n"
useradd -d /opt/webapp -s /usr/sbin/nologin webapp

echo -e "\nUpdating packages...\n"
apt update

echo -e "\nInstalling package prerequisites...\n"
apt install -y gunicorn nginx python3-flask libnginx-mod-http-modsecurity libmodsecurity3t64 python3-gunicorn python3-jwt python3-flaskext.wtf

echo -e "\nConfiguring nginx...\n"
cp nginx-site.conf /etc/nginx/sites-available/default

# Disable the IncludeOptional directives, because they're somehow broken and cause nginx to fail startup.
sed -i 's/^IncludeOptional /#IncludeOptional /g' /usr/share/modsecurity-crs/owasp-crs.load
systemctl reload nginx

echo -e "\nConfiguring registering webapp with systemd...\n"

# Reset the database directory, and ensure it is writeable by the gunicorn process.
rm -rf /opt/webapp/instance
mkdir -m 0700 /opt/webapp/instance
chown webapp:webapp /opt/webapp/instance

cp flask-webapp.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable flask-webapp
systemctl start flask-webapp

echo -e "\nDone!"
