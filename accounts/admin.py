from django.contrib import admin
from .models import CustomUser, CreatorProfile

admin.site.register(CustomUser)
admin.site.register(CreatorProfile)
