from django.contrib import admin
from main import models


admin.site.register(models.Book)
admin.site.register(models.Rating)
admin.site.register(models.User)
