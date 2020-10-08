from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# Cities

# Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    current_city = models.CharField(max_length=25)
    image = models.CharField(max_length=500, default="https://www.flaticon.com/svg/static/icons/svg/3288/3288532.svg")
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

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
