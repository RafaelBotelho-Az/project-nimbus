from django.contrib import admin
from nimbus import models

@admin.register(models.Art)
class ArtAdmin(admin.ModelAdmin):
    list_display = 'artist', 'title', 'image', 'created_date', 

@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = 'user', 'profile_image', 

@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    ...
