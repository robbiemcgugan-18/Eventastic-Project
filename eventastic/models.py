from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    description = models.CharField(max_length=200)
    picture = models.ImageField(upload_to='category_images/', blank=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    DOB = models.DateField()
    profilePicture = models.ImageField(upload_to='profile_images/', blank=True)

    def __str__(self):
        return self.user.username

class Event(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    description = models.CharField(max_length=200)
    start = models.DateField(default=None)
    usersInterested = models.ManyToManyField(UserProfile,blank=True,related_name='interest')
    numberInterested = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='event_images/', blank=True)
    address = models.CharField(max_length=40)
    postcode = models.CharField(max_length=8)
    averageRating = models.DecimalField(max_digits=3, decimal_places=2,default=0)
    createdBy = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Comment(models.Model):
    name = models.ForeignKey(Event, on_delete=models.CASCADE)
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    posted = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} {self.name} {self.posted}"
