"""
WSGI config for socket_practice project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import socketio
import eventlet
import eventlet.wsgi

from chat.views import sio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_example.settings")

django_app = get_wsgi_application()
application = socketio.WSGIApp(sio, django_app)
eventlet.wsgi.server(eventlet.listen(('', 8000)), application)
