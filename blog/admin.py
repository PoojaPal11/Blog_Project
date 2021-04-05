from django.contrib import admin
from blog import models

admin.site.register(models.UserProfile)
admin.site.register(models.Post)
admin.site.register(models.Comment)
