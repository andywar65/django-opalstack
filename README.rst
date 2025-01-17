django-opalstack
================

Django interface to Opalstack python API

What is (((Opalstack?
---------------------

`(((Opalstack.com <https://opalstack.com>`__ is a developer friendly
hosting company. It has a powerful
`API <https://my.opalstack.com/api/v1/doc/>`__ that enables full control
over one's hosting environment. A `python
wrapper <https://github.com/opalstack/opalstack-python>`__ is provided
for the API.

Requirements
------------

This app is tested on Django 5.1 and Python 3.12. It requires the
aforementioned python API and the
`requests <https://requests.readthedocs.io/en/latest/>`__ library.
`HTMX <https://htmx.org>`__ is injected for smooth interactions
(JavaScript must be enabled in your browser).

Installation from PyPI
----------------------

Activate your virtual environment and install with:

::

   python -m pip install django-opalstack

In your Django project add:

.. code:: python

   INSTALLED_APPS = [
       # ...
       "django_opalstack",
   ]

.. code:: python

   # my_project/urls.py
   urlpatterns = [
       # ...
       path("opal/", include("django_opalstack.urls", namespace="django_opalstack")),
   ]

Finally run the following management commands:

::

   python manage.py migrate
   python manage.py collectstatic

Templates
~~~~~~~~~

You also need a ``base.html`` template with following template blocks (a
sample ``base.html`` is provided among package templates).

::

   {% block content %}
   {% endblock content %}
   ...
   {% block extra-js %}
   {% end block extra-js %}

Package comes with several templates in the
``django_opalstack/templates/`` directory. All templates have very few
styles (all inline). If you want to add your own styles, copy the
templates in a new ``my_project/templates/django_opalstack/`` directory
and override them. You will have to set:

.. code:: python

   TEMPLATES = [
       {
           "BACKEND": "django.template.backends.django.DjangoTemplates",
           "DIRS": [BASE_DIR / "my_project/templates"],
           # ...
       },
   ]

Usage
-----

You will need an `(((Opalstack.com <https://opalstack.com>`__ account
(there is a 14-day free trial). Once logged in, obtain a API token from
https://my.opalstack.com/tokens/. Copy the token ``KEY``, then run the
local server and browse to
http://128.1.1.0:8000/admin/django_opalstack/token/add/ and create a new
``Token`` pasting the previously copied ``KEY``. Go to
http://128.1.1.0:8000/opal/token/ and select the newly added token. At
the moment the app is read only, you will have to create ``OS users``,
``Applications`` and ``Sites`` directly on Opalstack.

Tests
-----

Tests with unittest, 99% coverage. Tested for Django 5.1 and Python 3.12
versions.

Changelog
---------

-  0.1.0: First working version (read only)
