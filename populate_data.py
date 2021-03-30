import datetime
import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventastic_project.settings')

django.setup()

from eventastic.models import User, UserProfile, Category, Event, Comment


def clear_db():
    UserProfile.objects.filter().delete()
    User.objects.filter().delete()
    Category.objects.filter().delete()


def generate_data():
    # generate 3 user
    user1 = User(username="John", email="john@example.com")
    user2 = User(username="Marry", email="mary@example.com")
    user3 = User(username="Kate", email="kate@example.com")
    for user_ins in [user1, user2, user3]:
        user_ins.set_password("maggie05")
        user_ins.save()
    # generate 3 user profile
    profile1 = UserProfile(user=user1, DOB=datetime.datetime(1990, 1, 1))
    profile2 = UserProfile(user=user2, DOB=datetime.datetime(1995, 1, 1))
    profile3 = UserProfile(user=user3, DOB=datetime.datetime(2000, 1, 1))
    for profile_ins in [profile1, profile2, profile3]:
        profile_ins.save()
    # generate multiple category
    # Prepare an image for each category and place it in category_images
    aviation_category = Category(name="Aviation", description="Here is Aviation description", picture="Aviation.jpg")
    bake_sales_category = Category(name="Bake Sales", description="Here is Bake Sales description",
                                   picture="Bake Sales.jpg")
    cooking_category = Category(name="Cooking", description="Here is Cooking description", picture="Cooking.jpg")
    aviation_category.save()
    bake_sales_category.save()
    cooking_category.save()
    # generate multiple event
    # Each event also prepares an image to be placed in event_images
    event1 = Event(name="aviation event1", description="aviation event1 description",
                   start=datetime.datetime(2020, 1, 1), picture="aviation event1.jpeg", address="New York",
                   postcode="00000001", averageRating=2.5, createdBy=profile3, category=aviation_category)
    event2 = Event(name="bake sales event1", description="bake sales event1 description",
                   start=datetime.datetime(2020, 2, 1), picture="bake sales event1.jpeg", address="New York",
                   postcode="00000002", averageRating=1.5, createdBy=profile1, category=bake_sales_category)
    event3 = Event(name="cooking event1", description="cooking event1 description",
                   start=datetime.datetime(2020, 3, 1), picture="cooking event1.jpeg", address="New York",
                   postcode="00000003", averageRating=2.0, createdBy=profile2, category=cooking_category)
    event1.save()
    event2.save()
    event3.save()
    # user interested m2m many to many
    event1.usersInterested.add(profile1)
    event1.usersInterested.add(profile2)
    event2.usersInterested.add(profile2)
    event2.usersInterested.add(profile3)
    event3.usersInterested.add(profile1)
    event3.usersInterested.add(profile3)
    event1.numberInterested = 2
    event2.numberInterested = 2
    event3.numberInterested = 2
    event1.save()
    event2.save()
    event3.save()
    # generate comment
    Comment(name=event1, username=profile1, comment="event1 is so nice").save()
    Comment(name=event2, username=profile1, comment="event2 is just so so").save()
    Comment(name=event1, username=profile2, comment="I think event2 is ok").save()
    Comment(name=event1, username=profile2, comment="I think event1 is nice").save()
    Comment(name=event3, username=profile3, comment="event3 is well").save()
    Comment(name=event3, username=profile2, comment="event3 is good").save()


if __name__ == "__main__":
    clear_db()
    generate_data()
