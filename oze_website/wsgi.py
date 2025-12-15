"""
WSGI config for OZE Website project.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oze_website.settings.prod')

application = get_wsgi_application()
