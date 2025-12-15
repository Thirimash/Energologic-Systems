#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Auto-detect production environment (Railway, Heroku, etc.)
    # Use prod settings if DATABASE_URL or RAILWAY_ENVIRONMENT is set
    if os.environ.get('DATABASE_URL') or os.environ.get('RAILWAY_ENVIRONMENT'):
        default_settings = 'oze_website.settings.prod'
    else:
        default_settings = 'oze_website.settings.dev'
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', default_settings)
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
