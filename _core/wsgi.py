"""WSGI entry point for a Python host such as Gunicorn."""
import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', '_core.settings')
application = get_wsgi_application()
