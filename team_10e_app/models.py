from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone
from django.contrib.auth.models import User

class Category(models.Model):
    categoryName = models.CharField(max_length=30, unique=True)
    categoryPicture = models.ImageField()
    categoryDescription = models.CharField(max_length=200)

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
    eventName = models.CharField(max_length=30, unique=True)
    eventDescription = models.CharField(max_length=200)
    start = models.DateTimeField()
    numberInterested = models.IntegerField()
    eventPicture = models.ImageField()
    address = models.CharField(max_length=40)
    postcode = models.CharField(max_length=8)
    averageRating = models.DecimalField(max_digits=3, decimal_places=2)
    createdBy = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.eventName

class Attend(models.Model):
    eventName = models.ForeignKey(Event, on_delete=models.CASCADE)
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    class Meta:
        UniqueConstraint(fields=['eventName', 'username'], name='userAttends')

    def __str__(self):
        return f"{self.username} {self.eventName}"

class Comment(models.Model):
    eventName = models.ForeignKey(Event, on_delete=models.CASCADE)
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    posted = models.DateTimeField(default=timezone.now())
    comment = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} {self.eventName} {self.posted}"