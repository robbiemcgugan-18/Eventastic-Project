from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Model that stores data about a user profile
# Fields:
# user - associated instance of the User table
# DOB - date of birth of user
# profilePicture - profile picture of the user
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    DOB = models.DateField()
    profilePicture = models.ImageField(upload_to='profile_images/', blank=True)

    def __str__(self):
        return self.user.username

# Model that stores data about a category
# Fields:
# name - name of the category
# description - description of the category
# picture - picture of the category
# slug - uses slugify that format the category name to be used appropiately in the URL
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

# Model that stores data about an event
# Fields:
# name - name of the event
# description - description of the event
# startDate - date of the event
# startTime - start time of the event
# usersInterested - Many to Many field that stores the users that are interested in the event
# numberInterested - number of users that are interested in the event
# picture - picture of the category
# address - address of the event
# postcode - postcode of the event
# createdBy - the user profile that created the event
# created - the time at which the event was created
# category - the category of the event
# slug - uses slugify that format the event name to be used appropiately in the URL
class Event(models.Model):
    name = models.CharField(max_length=30, primary_key=True)
    description = models.CharField(max_length=200)
    startDate = models.DateField()
    startTime = models.TimeField()
    usersInterested = models.ManyToManyField(UserProfile,blank=True,related_name='interest')
    numberInterested = models.IntegerField(default=0)
    picture = models.ImageField(upload_to='event_images/', blank=True)
    address = models.CharField(max_length=40)
    postcode = models.CharField(max_length=8)
    createdBy = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

# Model that stores data about a comment
# Fields:
# eventName - event the comment is for
# username - user who made the comment
# posted - the time at which the comment was made
# comment - the actual comment
class Comment(models.Model):
    eventName = models.ForeignKey(Event, on_delete=models.CASCADE)
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    posted = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.username} commented on {self.name} at {self.posted}"
