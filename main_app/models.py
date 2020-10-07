from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

# Cities

# Profile
class Profile(models.Model):
    name = models.CharField(min_length=1, max_length=25, default=user)
    city = models.CharField(min_length=1, max_length=25)
    image = models.CharField(max_length=500)
    join_date = datetime.now()
    user = models.OneToOneField(User)

    def __str__(self):
        return self.name

# Posts
class Post(models.Model):
    title = models.CharField(min_length=1, max_length=200)
    body = models.TextField(min_length=1, max_length=1000)
    date = datetime.now()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']