from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here

# City
class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    image = models.CharField(max_length=250)

    def __str__(self):
        return self.name

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
def update_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

# Posts
class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(max_length=1000)
    post_date = models.DateTimeField(auto_now_add=True)
    city = models.OneToOneField(City, on_delete=models.CASCADE, related_name="city")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} posted {self.post_date}"

    class Meta:
        ordering = ['-post_date']


