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
    title = models.CharField(max_length=80, verbose_name='Título')
    description = models.TextField(max_length=255, verbose_name='Descrição')
    image = models.ImageField(upload_to='art_images/', verbose_name='Imagem')
    artist = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True)
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def total_comments(self):
        return self.comments.count()

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    
class Like(models.Model):
    art = models.ForeignKey(
        Art, on_delete=models.CASCADE, related_name='likes'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='likes'
    )
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} liked {self.art.title}"

    class Meta:
        unique_together = ('art', 'user')


class Comment(models.Model):
    art = models.ForeignKey(
        Art, on_delete=models.CASCADE, related_name='comments'
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    comment = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} commented on {self.art.title}"