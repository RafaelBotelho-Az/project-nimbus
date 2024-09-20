from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.utils import timezone
from django.db import models



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(
        upload_to='profile_images/',
        blank=True,
        null=True
    )
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username

class Art(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='art_images/')
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
    

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name