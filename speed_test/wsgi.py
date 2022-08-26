"""
WSGI config for speed_test project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
import sys
# sys.path.append('/opt/bitnami/projects/speed_test')
# os.environ.setdefault("PYTHON_EGG_CACHE", "/opt/bitnami/apps/django/django_projects/speed_test/egg_cache")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "speed_test.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
