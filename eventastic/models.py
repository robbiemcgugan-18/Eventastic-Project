from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=200)
    picture = models.ImageField()
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.categoryName


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    DOB = models.DateField()
    profilePicture = models.ImageField()

    def __str__(self):
        return self.user.username

class Event(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=200)
    start = models.DateTimeField()
    numberInterested = models.IntegerField()
    picture = models.ImageField()
    address = models.CharField(max_length=40)
    postcode = models.CharField(max_length=8)
    averageRating = models.DecimalField(max_digits=3, decimal_places=2)
    createdBy = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.eventName

class Attend(models.Model):
    name = models.ForeignKey(Event, on_delete=models.CASCADE)
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    class Meta:
        UniqueConstraint(fields=['eventName', 'username'], name='userAttends')

    def __str__(self):
        return f"{self.username} {self.eventName}"

class Comment(models.Model):
    name = models.ForeignKey(Event, on_delete=models.CASCADE)
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    posted = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} {self.eventName} {self.posted}"
