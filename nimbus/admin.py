from django.contrib import admin
from nimbus import models

@admin.register(models.Art)
class ArtAdmin(admin.ModelAdmin):
    ...

@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    ...
