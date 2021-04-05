from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    prof_url = models.URLField()
    prof_pic = models.ImageField(upload_to='prof_pics')

    def __str__(self):
        return self.user.username


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse('index')

    def __str__(self):
        return self.title + str(self.pk)


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='Comments')
    author = models.CharField(
        max_length=256, unique=True, blank=False, null=False)
    text = models.TextField()

    def __str__(self):
        return self.author
  