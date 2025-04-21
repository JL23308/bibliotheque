from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Livre)
admin.site.register(models.Auteur)
admin.site.register(models.Categorie)
