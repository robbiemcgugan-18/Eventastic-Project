import os
import importlib
import tempfile
import eventastic.models
from eventastic import forms
from django import forms as django_forms
from django.db import models
from django.urls import reverse
from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import fields as django_fields


FAILURE_HEADER = f"{os.linesep}{os.linesep}{os.linesep}================{os.linesep}Eventastic Failure{os.linesep}================{os.linesep}"
FAILURE_FOOTER = f"{os.linesep}"

def create_user_object():
    """
    Helper function to create a User object.
    """
    user = User.objects.get_or_create(username='john',
                                      first_name='john',
                                      last_name='doe',
                                      email='john.doe@example.com')[0]
    user.set_password('123456')
    user.save()

    return user

def create_user_profile_object():
    """
    Helper function to create a User Profile object.
    """
    user_profile = eventastic.models.UserProfile.objects.get_or_create(
                                                                       DOB='1990-01-01',
                                                                       profilePicture=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                                                                       user=create_user_object())[0]
    user_profile.save()
    return user_profile

def create_category_object():
    """
    Helper function to create a Category object.
    """
    category = eventastic.models.Category.objects.get_or_create(name='category1',
                                                                description='description1',
                                                                picture=tempfile.NamedTemporaryFile(suffix=".jpg").name)[0]
    category.save()
    return category

def create_event_object():
    """
    Helper function to create a User Profile object.
    """
    event = eventastic.models.Event.objects.get_or_create(name='event1',
                                                             description='description1',
                                                             startDate='2020-03-01',
                                                             startTime='10:00',
                                                             picture=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                                                             address='Address test',
                                                             postcode='000000',
                                                             category=create_category_object(),
                                                             createdBy=create_user_profile_object())[0]
    event.save()
    return event

class ViewsTests(TestCase):

    def setUp(self):
        self.views_module = importlib.import_module('eventastic.views')
        self.views_module_listing = dir(self.views_module)

        self.project_urls_module = importlib.import_module('eventastic.urls')

    def test_views_exist(self):
        """
        Checks the index view exists and is callable
        """
        index_exists = 'index' in self.views_module_listing
        self.assertTrue(index_exists, f"{FAILURE_HEADER}The index() view for eventastic does not exist.{FAILURE_FOOTER}")

        index_callable = callable(self.views_module.index)
        self.assertTrue(index_callable, f"{FAILURE_HEADER}The index() view for eventastic isn't callable.{FAILURE_FOOTER}")

        """
        Checks the register view exists and is callable
        """
        register_exists = 'register' in self.views_module_listing
        self.assertTrue(register_exists, f"{FAILURE_HEADER}The register() view for eventastic does not exist.{FAILURE_FOOTER}")

        register_callable = callable(self.views_module.register)
        self.assertTrue(register_callable, f"{FAILURE_HEADER}The register() view for eventastic isn't callable.{FAILURE_FOOTER}")

        """
        Checks the user_login view exists and is callable
        """
        user_login_exists = 'user_login' in self.views_module_listing
        self.assertTrue(user_login_exists, f"{FAILURE_HEADER}The user_login() view for eventastic does not exist.{FAILURE_FOOTER}")

        user_login_callable = callable(self.views_module.user_login)
        self.assertTrue(user_login_callable, f"{FAILURE_HEADER}The user_login() view for eventastic isn't callable.{FAILURE_FOOTER}")

        """
        Checks the user_logout view exists and is callable
        """
        user_logout_exists = 'user_logout' in self.views_module_listing
        self.assertTrue(user_logout_exists, f"{FAILURE_HEADER}The user_logout() view for eventastic does not exist.{FAILURE_FOOTER}")

        user_logout_callable = callable(self.views_module.user_logout)
        self.assertTrue(user_logout_callable, f"{FAILURE_HEADER}The user_logout() view for eventastic isn't callable.{FAILURE_FOOTER}")

        """
        Checks the show_category view exists and is callable
        """
        show_category_exists = 'show_category' in self.views_module_listing
        self.assertTrue(show_category_exists, f"{FAILURE_HEADER}The show_category() view for eventastic does not exist.{FAILURE_FOOTER}")

        show_category_callable = callable(self.views_module.show_category)
        self.assertTrue(show_category_callable, f"{FAILURE_HEADER}The show_category() view for eventastic isn't callable.{FAILURE_FOOTER}")

        """
        Checks the create_category view exists and is callable
        """
        create_category_exists = 'create_category' in self.views_module_listing
        self.assertTrue(create_category_exists, f"{FAILURE_HEADER}The create_category() view for eventastic does not exist.{FAILURE_FOOTER}")

        create_category_callable = callable(self.views_module.create_category)
        self.assertTrue(create_category_callable, f"{FAILURE_HEADER}The create_category() view for eventastic isn't callable.{FAILURE_FOOTER}")

        """
        Checks the show_event view exists and is callable
        """
        show_event_exists = 'show_event' in self.views_module_listing
        self.assertTrue(show_event_exists, f"{FAILURE_HEADER}The show_event() view for eventastic does not exist.{FAILURE_FOOTER}")

        show_event_callable = callable(self.views_module.show_event)
        self.assertTrue(show_category_callable, f"{FAILURE_HEADER}The show_event() view for eventastic isn't callable.{FAILURE_FOOTER}")

        """
        Checks the create_event view exists and is callable
        """
        create_event_exists = 'create_event' in self.views_module_listing
        self.assertTrue(create_event_exists, f"{FAILURE_HEADER}The create_event() view for eventastic does not exist.{FAILURE_FOOTER}")

        create_event_callable = callable(self.views_module.create_event)
        self.assertTrue(create_event_callable, f"{FAILURE_HEADER}The create_event() view for eventastic isn't callable.{FAILURE_FOOTER}")

        """
        Checks the categories view exists and is callable
        """
        categories_exist = 'categories' in self.views_module_listing
        self.assertTrue(categories_exist, f"{FAILURE_HEADER}The categories() view for eventastic does not exist.{FAILURE_FOOTER}")

        categories_callable = callable(self.views_module.categories)
        self.assertTrue(categories_callable, f"{FAILURE_HEADER}The categories() view for eventastic isn't callable.{FAILURE_FOOTER}")

        """
        Checks the account view exists and is callable
        """
        account_exists = 'account' in self.views_module_listing
        self.assertTrue(account_exists, f"{FAILURE_HEADER}The account() view for eventastic does not exist.{FAILURE_FOOTER}")

        account_callable = callable(self.views_module.account)
        self.assertTrue(account_callable, f"{FAILURE_HEADER}The account() view for eventastic isn't callable.{FAILURE_FOOTER}")

        """
        Checks the edit_account view exists and is callable
        """
        edit_account_exists = 'edit_account' in self.views_module_listing
        self.assertTrue(edit_account_exists, f"{FAILURE_HEADER}The edit_account() view for eventastic does not exist.{FAILURE_FOOTER}")

        edit_account_callable = callable(self.views_module.edit_account)
        self.assertTrue(edit_account_callable, f"{FAILURE_HEADER}The edit_account() view for eventastic isn't callable.{FAILURE_FOOTER}")

        """
        Checks the delete_account view exists and is callable
        """
        delete_account_exists = 'delete_account' in self.views_module_listing
        self.assertTrue(delete_account_exists, f"{FAILURE_HEADER}The delete_account() view for eventastic does not exist.{FAILURE_FOOTER}")

        delete_account_callable = callable(self.views_module.delete_account)
        self.assertTrue(delete_account_callable, f"{FAILURE_HEADER}The delete_account() view for eventastic isn't callable.{FAILURE_FOOTER}")

        """
        Checks the contact_us view exists and is callable
        """
        contact_us_exists = 'contact_us' in self.views_module_listing
        self.assertTrue(contact_us_exists, f"{FAILURE_HEADER}The contact_us() view for eventastic does not exist.{FAILURE_FOOTER}")

        contact_us_callable = callable(self.views_module.contact_us)
        self.assertTrue(contact_us_callable, f"{FAILURE_HEADER}The contact_us() view for eventastic isn't callable.{FAILURE_FOOTER}")

        """
        Checks the interest view exists and is callable
        """
        interest_exists = 'interest' in self.views_module_listing
        self.assertTrue(interest_exists, f"{FAILURE_HEADER}The interest() view for eventastic does not exist.{FAILURE_FOOTER}")

        interest_callable = callable(self.views_module.interest)
        self.assertTrue(interest_callable, f"{FAILURE_HEADER}The interest() view for eventastic isn't callable.{FAILURE_FOOTER}")

        """
        Checks the find_users view exists and is callable
        """
        find_users_exists = 'find_users' in self.views_module_listing
        self.assertTrue(find_users_exists, f"{FAILURE_HEADER}The find_users() view for eventastic does not exist.{FAILURE_FOOTER}")

        find_users_callable = callable(self.views_module.find_users)
        self.assertTrue(find_users_callable, f"{FAILURE_HEADER}The find_users() view for eventastic isn't callable.{FAILURE_FOOTER}")

        """
        Checks the show_user_events view exists and is callable
        """
        show_user_events_exists = 'show_user_events' in self.views_module_listing
        self.assertTrue(show_user_events_exists, f"{FAILURE_HEADER}The show_user_events() view for eventastic does not exist.{FAILURE_FOOTER}")

        show_user_events_callable = callable(self.views_module.show_user_events)
        self.assertTrue(show_user_events_callable, f"{FAILURE_HEADER}The show_user_events() view for eventastic isn't callable.{FAILURE_FOOTER}")

    def test_url_mapping(self):
        index_mapping_exists = False
        register_mapping_exists = False
        user_login_mapping_exists = False
        user_logout_mapping_exists = False
        show_category_mapping_exists = False
        create_category_mapping_exists = False
        show_event_mapping_exists = False
        create_event_mapping_exists = False
        categories_mapping_exists = False
        account_mapping_exists = False
        edit_account_mapping_exists = False
        delete_account_mapping_exists = False
        contact_us_mapping_exists = False
        interest_mapping_exists = False
        find_users_mapping_exists = False
        show_user_events_mapping_esists = False

        for mapping in self.project_urls_module.urlpatterns:
            if hasattr(mapping, 'name'):
                if mapping.name == 'index':
                    index_mapping_exists = True
                elif mapping.name == 'register':
                    register_mapping_exists = True
                elif mapping.name == 'login':
                    user_login_mapping_exists = True
                elif mapping.name == 'logout':
                    user_logout_mapping_exists = True
                elif mapping.name == 'show_category':
                    show_category_mapping_exists = True
                elif mapping.name == 'create_category':
                    create_category_mapping_exists = True
                elif mapping.name == 'show_event':
                    show_event_mapping_exists = True
                elif mapping.name == 'create_event':
                    create_event_mapping_exists = True
                elif mapping.name == 'categories':
                    categories_mapping_exists = True
                elif mapping.name == 'account':
                    account_mapping_exists = True
                elif mapping.name == 'edit_account':
                    edit_account_mapping_exists = True
                elif mapping.name == 'delete_account':
                    delete_account_mapping_exists = True
                elif mapping.name == 'contact_us':
                    contact_us_mapping_exists = True
                elif mapping.name == 'interest':
                    interest_mapping_exists = True
                elif mapping.name == 'find_users':
                    find_users_mapping_exists = True
                elif mapping.name == 'show_user_events':
                    show_user_events_mapping_esists = True

        self.assertTrue(index_mapping_exists, f"{FAILURE_HEADER}The index URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('eventastic:index'), '/eventastic/', f"{FAILURE_HEADER}The index URL lookup failed.{FAILURE_FOOTER}")

        self.assertTrue(register_mapping_exists, f"{FAILURE_HEADER}The register URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('eventastic:register'), '/eventastic/register/', f"{FAILURE_HEADER}The register URL lookup failed.{FAILURE_FOOTER}")

        self.assertTrue(user_login_mapping_exists, f"{FAILURE_HEADER}The user_login URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('eventastic:login'), '/eventastic/login/', f"{FAILURE_HEADER}The user_login URL lookup failed.{FAILURE_FOOTER}")

        self.assertTrue(user_logout_mapping_exists, f"{FAILURE_HEADER}The user_logout URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('eventastic:logout'), '/eventastic/logout/', f"{FAILURE_HEADER}The user_logout URL lookup failed.{FAILURE_FOOTER}")

        self.assertTrue(show_category_mapping_exists, f"{FAILURE_HEADER}The show_category URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('eventastic:show_category', kwargs = {'category_name_slug': 'test'}), '/eventastic/categories/test/', f"{FAILURE_HEADER}The show_category URL lookup failed.{FAILURE_FOOTER}")

        self.assertTrue(create_category_mapping_exists, f"{FAILURE_HEADER}The create_category URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('eventastic:create_category'), '/eventastic/create-category/', f"{FAILURE_HEADER}The create_category URL lookup failed.{FAILURE_FOOTER}")

        self.assertTrue(show_event_mapping_exists, f"{FAILURE_HEADER}The show_event URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('eventastic:show_event', kwargs = {'category_name_slug': 'test', 'event_name_slug': 'test'}), '/eventastic/categories/test/test/', f"{FAILURE_HEADER}The show_event URL lookup failed.{FAILURE_FOOTER}")

        self.assertTrue(create_event_mapping_exists, f"{FAILURE_HEADER}The create_event URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('eventastic:create_event'), '/eventastic/create-event/', f"{FAILURE_HEADER}The create_event URL lookup failed.{FAILURE_FOOTER}")

        self.assertTrue(categories_mapping_exists, f"{FAILURE_HEADER}The categories URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('eventastic:categories'), '/eventastic/categories/', f"{FAILURE_HEADER}The categories URL lookup failed.{FAILURE_FOOTER}")

        self.assertTrue(account_mapping_exists, f"{FAILURE_HEADER}The account URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('eventastic:account'), '/eventastic/login/account/', f"{FAILURE_HEADER}The account URL lookup failed.{FAILURE_FOOTER}")

        self.assertTrue(edit_account_mapping_exists, f"{FAILURE_HEADER}The edit_account URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('eventastic:edit_account'), '/eventastic/login/account/edit/', f"{FAILURE_HEADER}The edit_account URL lookup failed.{FAILURE_FOOTER}")

        self.assertTrue(delete_account_mapping_exists, f"{FAILURE_HEADER}The delete_account URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('eventastic:delete_account'), '/eventastic/login/account/delete/', f"{FAILURE_HEADER}The delete URL lookup failed.{FAILURE_FOOTER}")

        self.assertTrue(contact_us_mapping_exists, f"{FAILURE_HEADER}The contact_us URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('eventastic:contact_us'), '/eventastic/contact-us/', f"{FAILURE_HEADER}The contact_us URL lookup failed.{FAILURE_FOOTER}")

        self.assertTrue(interest_mapping_exists, f"{FAILURE_HEADER}The interest URL mapping could not be found.{FAILURE_FOOTER}")
        # The interest view returns a JSON response instead of rendering a page and thus does not have a URL lookup

        self.assertTrue(find_users_mapping_exists, f"{FAILURE_HEADER}The find_users URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('eventastic:find_users'), '/eventastic/find-users/', f"{FAILURE_HEADER}The find_users URL lookup failed.{FAILURE_FOOTER}")

        self.assertTrue(show_user_events_mapping_esists, f"{FAILURE_HEADER}The show_user_events URL mapping could not be found.{FAILURE_FOOTER}")
        self.assertEquals(reverse('eventastic:show_user_events', kwargs={'user_slug': 'test'}), '/eventastic/find-users/test/', f"{FAILURE_HEADER}The show_user_events URL lookup failed.{FAILURE_FOOTER}")

class ModelTests(TestCase):

    def test_userprofile(self):
        self.assertTrue('UserProfile' in dir(eventastic.models))

        user_profile = eventastic.models.UserProfile()

        expected_attributes = {
            'DOB': '2002-01-01',
            'profilePicture': tempfile.NamedTemporaryFile(suffix=".jpg").name,
            'user': create_user_object(),
        }

        expected_types = {
            'DOB': models.fields.DateField,
            'profilePicture': models.fields.files.ImageField,
            'user': models.fields.related.OneToOneField,
        }

        found_count = 0

        for attr in user_profile._meta.fields:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1

                    self.assertEqual(type(attr), expected_types[attr_name], f"{FAILURE_HEADER}The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'.{FAILURE_FOOTER}")
                    setattr(user_profile, attr_name, expected_attributes[attr_name])

        self.assertEqual(found_count, len(expected_attributes.keys()), f"{FAILURE_HEADER}In the UserProfile model, we found {found_count} attributes, but were expecting {len(expected_attributes.keys())}.{FAILURE_FOOTER}")
        user_profile.save()

    def test_event(self):
        self.assertTrue('Event' in dir(eventastic.models))

        event = eventastic.models.Event()

        expected_attributes = {
            'name': 'Test',
            'description': 'Test Description',
            'category': create_category_object(),
            'startDate': '2022-01-01',
            'startTime': '15:00',
            'numberInterested': 0,
            'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name,
            'address': 'Glasgow',
            'postcode': 'G12 8QQ',
            'createdBy': create_user_profile_object(),
        }

        expected_types = {
            'name': models.fields.CharField,
            'description': models.fields.CharField,
            'category': models.fields.related.ForeignKey,
            'startDate': models.fields.DateField,
            'startTime': models.fields.TimeField,
            'numberInterested': models.fields.IntegerField,
            'picture': models.fields.files.ImageField,
            'address': models.fields.CharField,
            'postcode': models.fields.CharField,
            'createdBy': models.fields.related.ForeignKey,
        }

        found_count = 0

        for attr in event._meta.fields:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1

                    self.assertEqual(type(attr), expected_types[attr_name], f"{FAILURE_HEADER}The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'.{FAILURE_FOOTER}")
                    setattr(event, attr_name, expected_attributes[attr_name])

        self.assertEqual(found_count, len(expected_attributes.keys()), f"{FAILURE_HEADER}In the Event model, we found {found_count} attributes, but were expecting {len(expected_attributes.keys())}.{FAILURE_FOOTER}")
        event.save()

    def test_category(self):
        self.assertTrue('Category' in dir(eventastic.models))

        category = eventastic.models.Category()

        expected_attributes = {
            'name': 'Test',
            'description': 'Test Description',
            'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name,
        }

        expected_types = {
            'name': models.fields.CharField,
            'description': models.fields.CharField,
            'picture': models.fields.files.ImageField,
        }

        found_count = 0

        for attr in category._meta.fields:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1

                    self.assertEqual(type(attr), expected_types[attr_name], f"{FAILURE_HEADER}The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'.{FAILURE_FOOTER}")
                    setattr(category, attr_name, expected_attributes[attr_name])

        self.assertEqual(found_count, len(expected_attributes.keys()), f"{FAILURE_HEADER}In the Event model, we found {found_count} attributes, but were expecting {len(expected_attributes.keys())}.{FAILURE_FOOTER}")
        category.save()

    def test_comment(self):
        self.assertTrue('Comment' in dir(eventastic.models))

        user = User.objects.get_or_create(username='john1',
                                          first_name='john',
                                          last_name='doe',
                                          email='john.doe@example.com')[0]
        user.set_password('123456')

        user_profile = eventastic.models.UserProfile.objects.get_or_create(DOB='1990-01-01',
                                                                           profilePicture=tempfile.NamedTemporaryFile(suffix=".jpg").name,
                                                                           user=user)[0]

        comment = eventastic.models.Comment()
        event = create_event_object()

        expected_attributes = {
            'name': event,
            'username': user_profile,
            'comment': 'Test Comment',
        }

        expected_types = {
            'name': models.fields.related.ForeignKey,
            'username': models.fields.related.ForeignKey,
            'comment': models.fields.CharField,
        }

        found_count = 0

        for attr in comment._meta.fields:
            attr_name = attr.name

            for expected_attr_name in expected_attributes.keys():
                if expected_attr_name == attr_name:
                    found_count += 1

                    self.assertEqual(type(attr), expected_types[attr_name], f"{FAILURE_HEADER}The type of attribute for '{attr_name}' was '{type(attr)}'; we expected '{expected_types[attr_name]}'.{FAILURE_FOOTER}")
                    setattr(comment, attr_name, expected_attributes[attr_name])

        self.assertEqual(found_count, len(expected_attributes.keys()), f"{FAILURE_HEADER}In the Event model, we found {found_count} attributes, but were expecting {len(expected_attributes.keys())}.{FAILURE_FOOTER}")
        comment.save()

class RegisterFormTests(TestCase):

    def test_empty_registration_post_response(self):
        """
        Checks the POST response of the registration view.
        What if we submit a blank form?
        """
        request = self.client.post(reverse('eventastic:register'))
        content = request.content.decode('utf-8')

        self.assertTrue('<ul class="errorlist">' in content)

    def test_good_form_creation(self):
        """
        Tests the functionality of the forms.
        Creates a UserProfileForm and UserForm, and attempts to save them.
        Upon completion, we should be able to login with the details supplied.
        """
        user_data = {'username': 'testuser', 'first_name': 'test', 'last_name': 'user', 'email': 'test@test.com', 'password': 'test123', 'confirm_password': 'test123'}
        user_form = forms.UserForm(data=user_data)

        user_profile_data = {'DOB': '1995-01-01', 'profilePicture': tempfile.NamedTemporaryFile(suffix=".jpg").name}
        user_profile_form = forms.UserProfileForm(data=user_profile_data)

        self.assertTrue(user_form.is_valid(), f"{FAILURE_HEADER}The UserForm was not valid after entering the required data.{FAILURE_FOOTER}")
        self.assertTrue(user_profile_form.is_valid(), f"{FAILURE_HEADER}The UserProfileForm was not valid after entering the required data.{FAILURE_FOOTER}")

        user_object = user_form.save()
        user_object.set_password(user_data['password'])
        user_object.save()

        user_profile_object = user_profile_form.save(commit=False)
        user_profile_object.user = user_object
        user_profile_object.save()

        self.assertEqual(len(User.objects.all()), 1, f"{FAILURE_HEADER}We were expecting to see a User object created, but it didn't appear.{FAILURE_FOOTER}")
        self.assertEqual(len(eventastic.models.UserProfile.objects.all()), 1, f"{FAILURE_HEADER}We were expecting to see a UserProfile object created, but it didn't appear.{FAILURE_FOOTER}")
        self.assertTrue(self.client.login(username='testuser', password='test123'), f"{FAILURE_HEADER}We couldn't log our sample user in during the tests.{FAILURE_FOOTER}")

    def test_duplicate_username(self):
        """
        Tests the functionality of the forms.
        Creates a UserProfileForm and UserForm, and attempts to save them.
        Upon completion, we should be able to login with the details supplied.
        """
        user_profile = create_user_profile_object()

        user_data = {'username': 'john', 'first_name': 'test', 'last_name': 'user', 'email': 'test@test.com', 'password': 'test123', 'confirm_password': 'test123'}
        user_profile_data = {'DOB': '1995-01-01', 'profilePicture': tempfile.NamedTemporaryFile(suffix=".jpg").name}

        data = {**user_data, **user_profile_data}

        request = self.client.post(reverse('eventastic:register'), data=data)
        content = request.content.decode('utf-8')

        self.assertTrue('<ul class="errorlist">' in content)

    def test_invalid_date(self):
        user_data = {'username': 'testuser', 'first_name': 'test', 'last_name': 'user', 'email': 'test@test.com', 'password': 'test123', 'confirm_password': 'test123'}
        user_profile_data = {'DOB': '1995-50-50', 'profilePicture': tempfile.NamedTemporaryFile(suffix=".jpg").name}

        data = {**user_data, **user_profile_data}

        request = self.client.post(reverse('eventastic:register'), data=data)
        content = request.content.decode('utf-8')

        self.assertTrue('<ul class="errorlist">' in content)

    def test_non_matching_passwords(self):
        user_data = {'username': 'testuser', 'first_name': 'test', 'last_name': 'user', 'email': 'test@test.com', 'password': 'test123', 'confirm_password': 'default'}
        user_profile_data = {'DOB': '1995-01-01', 'profilePicture': tempfile.NamedTemporaryFile(suffix=".jpg").name}

        data = {**user_data, **user_profile_data}

        request = self.client.post(reverse('eventastic:register'), data=data)
        content = request.content.decode('utf-8')

        self.assertRaises(django_forms.ValidationError)

    def test_invalid_email(self):
        user_data = {'username': 'testuser', 'first_name': 'test', 'last_name': 'user', 'email': 'test', 'password': 'test123', 'confirm_password': 'test123'}
        user_profile_data = {'DOB': '1995-01-01', 'profilePicture': tempfile.NamedTemporaryFile(suffix=".jpg").name}

        data = {**user_data, **user_profile_data}

        request = self.client.post(reverse('eventastic:register'), data=data)
        content = request.content.decode('utf-8')

        self.assertTrue('<ul class="errorlist">' in content)

class LoginFormTests(TestCase):
    def test_empty_login_form(self):
        """
        Checks the POST response of the registration view.
        What if we submit a blank form?
        """
        request = self.client.post(reverse('eventastic:login'))
        content = request.content.decode('utf-8')

        self.assertTrue('Username or Password is incorrect' in content)

    def test_good_login_form(self):

        user_profile = create_user_profile_object()

        login_data = {'username': 'john', 'password': '123456'}

        request = self.client.post(reverse('eventastic:login'), data=login_data)

        self.assertEqual(request.status_code, 302)

    def test_bad_username(self):

        user_profile = create_user_profile_object()

        login_data = {'username': 'random', 'password': '123456'}

        request = self.client.post(reverse('eventastic:login'), data=login_data)
        content = request.content.decode('utf-8')

        self.assertTrue('Username or Password is incorrect' in content)

    def test_bad_password(self):

        user_profile = create_user_profile_object()

        login_data = {'username': 'john', 'password': 'random'}

        request = self.client.post(reverse('eventastic:login'), data=login_data)
        content = request.content.decode('utf-8')

        self.assertTrue('Username or Password is incorrect' in content)

class CategoryFormTests(TestCase):
    def test_good_category_form(self):
        category_data = {'name': 'category', 'description': 'description1', 'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name}

        request = self.client.post(reverse('eventastic:create_category'), data=category_data)

        self.assertEqual(request.status_code, 302)


class EventFormTests(TestCase):
    def test_good_event_form(self):
        event_data = {'name': 'category', 'description': 'description1', 'startDate': '2021-03-01', 'startTime': '10:00', 'usersInterested': 0, 'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name, 'address': 'address', 'postcode': '000000', 'category': create_category_object(), 'createdBy': create_user_profile_object()}

        request = self.client.post(reverse('eventastic:create_event'), data=event_data)

        self.assertEqual(request.status_code, 302)

    def test_bad_date(self):
        event_data = {'name': 'category', 'description': 'description1', 'startDate': '2021-50-50', 'startTime': '10:00', 'usersInterested': 0, 'picture': tempfile.NamedTemporaryFile(suffix=".jpg").name, 'address': 'address', 'postcode': '000000', 'category': create_category_object(), 'createdBy': create_user_profile_object()}

        request = self.client.post(reverse('eventastic:create_event'), data=event_data)
        content = request.content.decode('utf-8')

        self.assertTrue('<ul class="errorlist">' in content)
