"""
WSGI config for chevrolet_uz project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chevrolet_uz.settings")
application = get_wsgi_application()
