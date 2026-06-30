import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chevrolet_uz.settings')
import django
django.setup()
from django.conf import settings
settings.ALLOWED_HOSTS.append('testserver')
from django.template import engines

engine = engines['django']
# Just render a raw csrf_token tag
t = engine.from_string('{% csrf_token %}')
from django.template import Context
ctx = Context({})
result = t.render(ctx)
print('Raw csrf_token render:', repr(result))
