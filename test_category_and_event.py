from django.test import TestCase
from django.urls import reverse

from eventastic.models import Event, Category


class EventTest(TestCase):

    def setUp(self):
        self.user_register()
        self.user_login()

    def user_register(self):
        username = "john"
        first_name = "john"
        last_name = "doe"
        email = "john.doe@example.com"
        password = "123456"
        dob = "1990-01-01"
        profile_picture = "test.jpg"
        self.client.post(
            reverse('eventastic:register'),
            data={"username": username, "first_name": first_name, "last_name": last_name,
                  "email": email, "password": password, "confirm_password": password, "DOB": dob,
                  "profilePicture": profile_picture})

    def user_login(self):
        response = self.client.post(reverse('eventastic:login'), data={"username": "john", "password": "123456"})

    def create_event(self):
        response = self.client.post(reverse("eventastic:create_event"), data={
            "category": "category1",
            "name": "event1",
            "description": "description1",
            "startDate": "2020-03-01",
            "startTime": "10:00",
            "address": "Address test",
            "postcode": "000000",
            "picture": "test.jpg"
        })
        event_ins = Event.objects.filter(name="event1").first()
        self.assertIsNotNone(event_ins)

    def create_category(self):
        response = self.client.post(reverse("eventastic:create_category"), data={
            "name": "category1",
            "description": "description1",
            "picture": "test.jpg"
        })
        category_ins = Category.objects.filter(name="category1").first()
        self.assertIsNotNone(category_ins)

    def test_category_and_event(self):
        self.create_category()
        self.create_event()
