from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
fs=FileSystemStorage(location='media/profile_image')

# Create your models here

# City
class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    image = models.CharField(max_length=250)
    slug = models.SlugField(max_length=25, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('cities_show', kwargs={'slug': self.slug})

    def __str__(self):
        return self.name

# Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    current_city = models.CharField(max_length=25)
    image = models.ImageField(upload_to='profile_image', default='profile_image/default_profile_photo.svg')
    join_date = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=25, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = self.slug or slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'slug': self.slug})

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
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="city")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} posted {self.post_date}"

    class Meta:
        ordering = ['-post_date']

# Comments
class Comment(models.Model):
    comment = models.TextField(max_length=500)
    comment_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    reply = models.ForeignKey('Comment', on_delete=models.CASCADE, null=True, related_name='replies', blank=True)
    #null=True to allow top comment without parent

    def __str__(self):
        return f"{self.comment} posted {self.comment_date}"

    class Meta:
        ordering = ['-comment_date']
