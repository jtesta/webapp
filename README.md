# Sample Flask Web Application

This is a sample web application written in Flask, which demonstrates JWT handling and SQL injection remediation with [ModSecurity](https://modsecurity.org/).

## Installation

As the root user on an Ubuntu Server 24.04 machine, checkout the source code into `/opt`:

```
# cd /opt
# git checkout https://github.com/jtesta/webapp
```

Next, create and edit the configuration file. Here the JWT ES256 public key and Google OIDC client ID is specified:

```
# cd /opt/webapp
# cp webapp.cfg.template webapp.cfg
# vim webapp.cfg  # Add public key and client ID
```

Lastly, run the `configure_host.sh` script to install all prerequisites and start all services:

```
# ./configure_host.sh
```

## Security Features

This application is intentionally vulnerable to SQL injection.  The `/page1` URI is fully unprotected.  The `/page2` URI is protected by the default ModSecurity settings.

By default (with a very limited set of exceptions), Flask applications are immune to XSS, [as per the documentation](https://flask.palletsprojects.com/en/stable/web-security/#cross-site-scripting-xss).

The service returns several security HTTP headers (see X).

The application does not use TLS by default, as hostname configuration and TLS certificate registration are rather complex.  This must be done manually.

Notably, the application does not protect against cross-site request forgery (CSRF).  Unfortunately, the [flask-wtf](https://github.com/pallets-eco/flask-wtf) module does not properly work as per its documentation without further workarounds (as documented [here](https://www.pythonanywhere.com/forums/topic/29833/) and [here](https://nickjanetakis.com/blog/fix-missing-csrf-token-issues-with-flask)).  Due to time limitations, this could not be completed.
