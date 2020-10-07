from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Cities

# Profile
class Profile(models.Model):
    name = models.CharField(max_length=25)
    # , default=user.username
    current_city = models.CharField(max_length=25)
    image = models.CharField(max_length=500)
    join_date = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Posts
class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=1000)
    post_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-post_date']