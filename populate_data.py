import datetime
import os

import django
from django.core.files.images import ImageFile

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
    user2 = User(username="Mary", email="mary@example.com")
    user3 = User(username="Kate", email="kate@example.com")
    for user_ins in [user1, user2, user3]:
        user_ins.set_password("maggie05")
        user_ins.save()
    # generate 3 user profile
    profile1 = UserProfile(user=user1, DOB=datetime.datetime(1990, 1, 1))
    profile2 = UserProfile(user=user2, DOB=datetime.datetime(1995, 1, 1))
    profile3 = UserProfile(user=user3, DOB=datetime.datetime(2000, 1, 1))

    profile1.profilePicture = ImageFile(open("default.jpg", 'rb'))
    profile2.profilePicture = ImageFile(open("default.jpg", 'rb'))
    profile3.profilePicture = ImageFile(open("default.jpg", 'rb'))

    for profile_ins in [profile1, profile2, profile3]:
        profile_ins.save()
    # generate multiple category
    # Prepare an image for each category and place it in category_images
    aviation_category = Category(name="Aviation", description="Here is Aviation description")
    cooking_category = Category(name="Cooking", description="Here is Cooking description")
    sport_category = Category(name="Sport", description="Here is Bake Sales description")

    aviation_category.picture = ImageFile(open("default.jpg", 'rb'))
    cooking_category.picture = ImageFile(open("default.jpg", 'rb'))
    sport_category.picture = ImageFile(open("default.jpg", 'rb'))

    aviation_category.save()
    cooking_category.save()
    sport_category.save()

    # generate multiple event
    # Each event also prepares an image to be placed in event_images
    aviation_event_1 = Event(name="Plane Spotting", description="Meet up to see the best planes arriving at the airport", startDate=datetime.datetime(2020, 1, 1), startTime=datetime.time(15, 00), address="Glasgow Airport",postcode="PA3 2TJ", createdBy=profile3, category=aviation_category)
    aviation_event_2 = Event(name="Air Show 2021", description="RAF is putting on an air show to entertain all ages", startDate=datetime.datetime(2020, 2, 1), startTime=datetime.time(15, 00), address="Prestwick Airport", postcode="KA9 2PL", createdBy=profile1, category=aviation_category)
    aviation_event_3 = Event(name="Aircraft Museum Tour", description="Volunteers are organising a guided tour of the nearby museum", startDate=datetime.datetime(2020, 3, 1), startTime=datetime.time(15, 00), address="East Fortune Airfield", postcode="EH39 5LF", createdBy=profile2, category=aviation_category)

    aviation_event_1.picture = ImageFile(open("population_images/event_images/aviation1.jpg", 'rb'))
    aviation_event_2.picture = ImageFile(open("population_images/event_images/aviation2.jpg", 'rb'))
    aviation_event_3.picture = ImageFile(open("population_images/event_images/aviation3.jpg", 'rb'))

    cooking_event_1 = Event(name="Cook Off 2021", description="Competition to see who is the best cook of 2021", startDate=datetime.datetime(2020, 1, 1), startTime=datetime.time(15, 00), address="8 East Fergus Place, Kirkcaldy",postcode="KY1 1XT", createdBy=profile1, category=cooking_category)
    cooking_event_2 = Event(name="Masterclass Lesson", description="Learn to cook like one of the best chefs in the country", startDate=datetime.datetime(2020, 2, 1), startTime=datetime.time(15, 00), address="8 East Fergus Place, Kirkcaldy", postcode="KY1 1XT", createdBy=profile1, category=cooking_category)
    cooking_event_3 = Event(name="Church Bake Sale", description="Come along to get some delicious home made cakes and biscuits", startDate=datetime.datetime(2020, 3, 1), startTime=datetime.time(15, 00), address="Eaglesham, Glasgow", postcode="G76 0AR", createdBy=profile2, category=cooking_category)

    cooking_event_1.picture = ImageFile(open("population_images/event_images/cooking1.jpg", 'rb'))
    cooking_event_2.picture = ImageFile(open("population_images/event_images/cooking2.jpg", 'rb'))
    cooking_event_3.picture = ImageFile(open("population_images/event_images/cooking3.jpg", 'rb'))

    sport_event_1 = Event(name="Football Meet up", description="Quick meet up to play a game of football", startDate=datetime.datetime(2020, 1, 1), startTime=datetime.time(15, 00), address="941, Pollokshaws Road, Glasgow",postcode="G41 2EU", createdBy=profile1, category=sport_category)
    sport_event_2 = Event(name="Tennis Tournament", description="Sign up to prove you are the best tennis player", startDate=datetime.datetime(2020, 2, 1), startTime=datetime.time(15, 00), address="130 Clyde Street, Glasgow", postcode="G1 4LH", createdBy=profile1, category=sport_category)
    sport_event_3 = Event(name="Basketball Session", description="Need a few more players to get a good game of basketball", startDate=datetime.datetime(2020, 3, 1), startTime=datetime.time(15, 00), address="196, Ayr Rd, Newton Mearns, Glasgow", postcode="G77 6DT", createdBy=profile2, category=sport_category)

    sport_event_1.picture = ImageFile(open("population_images/event_images/sport1.jpg", 'rb'))
    sport_event_2.picture = ImageFile(open("population_images/event_images/sport2.jpg", 'rb'))
    sport_event_3.picture = ImageFile(open("population_images/event_images/sport3.jpg", 'rb'))

    aviation_event_1.save()
    aviation_event_2.save()
    aviation_event_3.save()

    cooking_event_1.save()
    cooking_event_2.save()
    cooking_event_3.save()

    sport_event_1.save()
    sport_event_2.save()
    sport_event_3.save()

    # user interested m2m many to many
    cooking_event_1.usersInterested.add(profile1)
    cooking_event_2.usersInterested.add(profile2)

    cooking_event_1.save()
    cooking_event_2.save()
    sport_event_3.save()
    aviation_event_2.save()

    cooking_event_1.numberInterested = 1
    cooking_event_2.numberInterested = 1

    cooking_event_1.save()
    cooking_event_2.save()
    # generate comment
    Comment(name=cooking_event_1, username=profile1, comment="event1 is so nice").save()
    Comment(name=cooking_event_1, username=profile1, comment="event2 is just so so").save()
    Comment(name=aviation_event_2, username=profile2, comment="I think this looks ok").save()
    Comment(name=cooking_event_2, username=profile2, comment="I think event1 is nice").save()
    Comment(name=aviation_event_2, username=profile3, comment="event3 is well").save()
    Comment(name=sport_event_3, username=profile2, comment="event3 is good").save()


if __name__ == "__main__":
    clear_db()
    generate_data()
