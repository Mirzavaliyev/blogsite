import os
import sys

# Loyiha papkasini Python yo‘liga qo‘shish
sys.path.append(os.getcwd())

# Django sozlamalar modulini belgilash
os.environ['DJANGO_SETTINGS_MODULE'] = 'myblog.settings'

# Django WSGI ilovasini yuklash
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()