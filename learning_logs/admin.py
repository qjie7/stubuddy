from django.contrib import admin

# Register your models here.

# the dot in front of models tells Django to look for models.py in the same directory as admin.py
from .models import Topic, Entry

# tells Django to manage our model through the admin site
admin.site.register(Topic)
admin.site.register(Entry)
