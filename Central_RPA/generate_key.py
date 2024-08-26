import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Central_RPA.settings')
django.setup()

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

user = User.objects.get(username='teste')
token, created = Token.objects.get_or_create(user=user)
print(token)