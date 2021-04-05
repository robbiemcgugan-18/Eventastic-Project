from django.shortcuts import render, redirect
from eventastic.forms import UserForm, UserProfileForm, CategoryForm, EventForm, EditUserForm, EditProfileForm, DeleteUserForm, AddCommentForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from eventastic.models import Category, Event, UserProfile, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.views import View
from geopy import Nominatim
from django.core.files.images import ImageFile

"""
This view renders the home page onscreen
"""
def index(request):
    # Define empty context dictionary
    context_dict = {}

    # Get the 9 events with the most users interested and store them in the context dictionary
    top_events = Event.objects.order_by('-numberInterested')[:9]
    context_dict['top_events'] = top_events

    return render(request, 'eventastic/index.html', context=context_dict)

"""
This view renders the register page and form onscreen
"""
def register(request):
    # Define empty context dictionary
    context_dict = {}

    # If the method is POST (form has been submitted) the form will be processed
    if request.method == 'POST':
        # Get the information from the forms
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # if the form information is valid then the information will be saved
        if user_form.is_valid() and profile_form.is_valid():
            # Save the User form information in the database
            user = user_form.save()

            # Hash the saved password and resave it
            user.set_password(user.password)
            user.save()

            # Save the User Profile form information in the database
            profile = profile_form.save(commit=False)
            profile.user = user

            # If the user attaches a picture then save that picture as their profile picture
            if 'profilePicture' in request.FILES:
                profile.profilePicture = request.FILES['profilePicture']
            # Else use the default profile picture
            else:
                profile.profilePicture = ImageFile(open("static/images/default_profile_picture.jpg", 'rb'))

            # Finalise the changes to the user profile
            profile.save()

            # Login the newly registered user
            new_user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
            login(request, new_user)

            # Redirect the user to the home page
            return redirect(reverse('eventastic:index'))

        # If the form information is not valid then print error
        else:
            messages.error(request, "Form is invalid")

    # If the form has not been submitted display the form onscreen
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Add the forms to the context dictionary
    context_dict['user_form'] = user_form
    context_dict['profile_form'] = profile_form

    # Render the view onscreen using the given context
    return render(request, 'eventastic/register.html', context = context_dict)

"""
This view renders the user login page and form onscreen
"""
def user_login(request):

    # Define the context dictionary with an empty error message
    context_dict = {'error_message': None}

    # If the method is POST (form has been submitted) the form will be processed
    if request.method == 'POST':
        # Get the username and password values from the POST request
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Attempt to authenticate the user with the provided details
        user = authenticate(username=username, password=password)

        # If a user with the given username and password exists
        if user:
            # Check that their account is still active
            # If it is then log the user in
            if user.is_active:
                login(request, user)

                # Redirect the user back to the home page
                return redirect(reverse('eventastic:index'))

            # If the account exists but is disabled, display an error message
            else:
                context_dict['error_message'] = "Account is disabled"

        # If an account with the given details does not exist, display an error message
        else:
            context_dict['error_message'] = "Username or Password is incorrect"

    # If the form has not been submitted, render the view onscreen
    return render(request, 'eventastic/login.html', context=context_dict)


"""
This view logs out a logged in user
"""
@login_required
def user_logout(request):
    # Log the user out
    logout(request)

    # Redirect the user back to the home page
    return redirect(reverse('eventastic:index'))

"""
This view renders a page ccontaining information about a category onscreen
"""
def show_category(request, category_name_slug):
    # Define empty context dictionary
    context_dict = {}

    try:
        # Get the category with the given category_name_slug
        category = Category.objects.get(slug=category_name_slug)

        # Get all the events that come under that category
        events = Event.objects.filter(category=category)

        # store the category and events in the context dictionary
        context_dict['events'] = events
        context_dict['category'] = category

    # If a category with the given category_name_slug does not exist
    # then display None in the 'category' and 'events' spaces in context dictionary
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['events'] = None

    # Finally, render the view onscreen using the given context
    return render(request, 'eventastic/show_category.html', context=context_dict)

"""
This view renders the create category page and form onscreen
"""
@login_required
def create_category(request):
    # Define empty context dictionary
    context_dict = {}

    # If the method is POST (form has been submitted) the form will be processed
    if request.method == 'POST':
        # Get the data from the form
        form = CategoryForm(request.POST)

        # If the form information is valid then save the information in the database
        if form.is_valid():
            form_data = form.save(commit=False)

            if 'picture' in request.FILES:
                form_data.picture = request.FILES['picture']
            else:
                form_data.picture = ImageFile(open("static/images/category_and_event_default.jpg", 'rb'))

            form_data.save()

            # Get the slug for the created category
            category_name_slug = form_data.slug
            # Redirect the user to the page for that category using the slug
            return redirect('eventastic:show_category', category_name_slug=category_name_slug)

        # If the form information is not valid display the errors
        else:
            messages.error(request, form.errors)

    # Define the form that needs to be displayed onscreen
    form = CategoryForm()

    # Add the form to the context dictionary
    context_dict['form'] = form

    # If the form has not been submitted then render the view onscreen
    return render(request, 'eventastic/create_category.html', context=context_dict)

"""
This view renders a page containing information about an event onscreen
"""
def show_event(request, category_name_slug, event_name_slug):
    # Define empty context dictionary
    context_dict = {}

    try:
        # Get the event with the given event_name_slug
        event = Event.objects.get(slug=event_name_slug)
        # Store the event in the context dictionary
        context_dict['event'] = event

    # If an event with the given event_name_slug does not exist
    # then display None in the 'event' space in context dictionary
    except Event.DoesNotExist:
        context_dict['event'] = None

    try:
        # Get the currently logged in user
        user_profile = UserProfile.objects.get(user=request.user.id)
        # Check if that user is in the Many to Many field in the current event
        is_interested = event.usersInterested.filter(user=user_profile).exists()
        # Store a boolean value in the context dictionary indicating if the user is in the Many to Many field
        context_dict['is_interested'] = is_interested
    except:
        # If the user is not logged in set is_interested to False
        context_dict['is_interested'] = False

    # Create a locator using the geopy external library
    locator = Nominatim(user_agent="myGeocoder")

    try:
        # Get the location data about the postcode of the current event
        location = locator.geocode(event.postcode)

        # Store the latitude and longitude of the postcode to be used in the MapBox API
        context_dict['latitude'] = location.latitude
        context_dict['longitude'] = location.longitude

    except:
        # If the postcode is not valid then store None for the latitude and longitude
        context_dict['latitude'] = None
        context_dict['longitude'] = None

    # Get all the comments for the current event and store them in the context dictionary
    comments = Comment.objects.filter(eventName=event)
    context_dict['comments'] = comments

    # If the add comment form is submitted
    if request.method == 'POST':
        # If the user is not logged in redirect them to the login page
        if not request.user.is_authenticated:
            return redirect('eventastic:login')

        # Get the data from the form
        form = AddCommentForm(request.POST)

        # If the form is valid
        if form.is_valid():
            comment = form.save(commit=False)

            # set the event of the comment to the current event
            comment.eventName = event
            # Set the username to the current logged in user
            comment.username = user_profile

            # Save this information in the database
            comment.save()

            # Redirect the user
            return redirect('eventastic:show_event', event_name_slug=event_name_slug, category_name_slug=category_name_slug)

        else:
            # Else display an error
            messages.error(request, "Invalid Form")

    else:
        # If the form was not submitted then create an empty form
        form = AddCommentForm()

    # Add the form to the context dictionary
    context_dict['form'] = form

    # Render the view onscreen using the given context
    return render(request, 'eventastic/show_event.html', context=context_dict)

"""
This view renders the create event page and form onscreen
"""
@login_required
def create_event(request):
    # Define the form that needs to be displayed onscreen
    form = EventForm()

    # If the method is POST (form has been submitted) the form will be processed
    if request.method == 'POST':
        # Get the data from the form
        form = EventForm(request.POST)

        # If the form information is valid then save the information in the database
        if form.is_valid():
            # Set the createdBy field to the user that is currently logged in
            form.instance.createdBy = UserProfile.objects.get(user=request.user)
            # Save the form data to the database
            form_data = form.save(commit=False)

            if 'picture' in request.FILES:
                form_data.picture = request.FILES['picture']
            else:
                form_data.picture = ImageFile(open("static/images/category_and_event_default.jpg", 'rb'))

            form_data.save()

            # Get the slug for the created event
            event_name_slug = form_data.slug

            # Get the slug for the category the created event comes under
            category_obj = Category.objects.get(name=form_data.category)
            category_name_slug = category_obj.slug

            # Redirect the user to the page that shows the event using the two slugs
            return redirect('eventastic:show_event', category_name_slug=category_name_slug, event_name_slug=event_name_slug)

        # If the form information is not valid then display an error
        else:
            messages.error(request, "Form is invalid")

    # If the form has not been submitted then render the view onscreen
    return render(request, 'eventastic/create_event.html', context={'form': form})

"""
This view renders the page that shows all the categories onscreen
"""
def categories(request):
    # Define empty context dictionary
    context_dict = {}

    # Order the categories by name (A-Z) and store them in the context dictionary
    categories = Category.objects.order_by('name')
    context_dict['categories'] = categories

    # Render the view onscreen using the given context
    return render(request, 'eventastic/categories.html', context=context_dict)

"""
This view renders the page that displays the user account details onscreen
"""
@login_required
def account(request):
    # Define empty context dictionary
    context_dict = {}

    # If the method is POST (password change form has been submitted) the form will be processed
    if request.method == 'POST':
        # Get the data from the password change form
        form = PasswordChangeForm(request.user, request.POST)

        # If the form is valid
        if form.is_valid():
            # Save the updated password
            updated_password = form.save()
            # Update the password hash
            update_session_auth_hash(request, updated_password)
            # Redirect the user back to the account page
            return redirect('eventastic:account')

        else:
            # If the form is not valid then display an error message
            messages.error(request, "Form is invalid")

    else:
        # If the form was not submitted then create an empty form
        form = PasswordChangeForm(request.user)

    # Store the form in the context dictionary
    context_dict['form'] = form

    # Get the user profile of the logged in user
    user_profile = UserProfile.objects.get(user=request.user.id)
    # Get all the events that the user has organised
    organised_events = Event.objects.filter(createdBy=user_profile)

    # Get all the events the current user is interested in
    interested_events = []
    for event in Event.objects.all():
        if event.usersInterested.filter(user=user_profile).exists():
            interested_events.append(event)

    # Store the current user profile, the events the user has organised
    # and the events the user is interested in, in the context dictionary
    context_dict['user_profile'] = user_profile
    context_dict['organised_events'] = organised_events
    context_dict['interested_events'] = interested_events

    # Render the view onscreen using the given context
    return render(request, 'eventastic/account.html', context=context_dict)

"""
This view renders the page and form that allows the user to update their details onscreen
"""
@login_required
def edit_account(request):
    # Define empty context dictionary
    context_dict = {}
    # Get the user profile of the logged in user
    user_profile = UserProfile.objects.get(user=request.user.id)

    # If the method is POST (form has been submitted) the form will be processed
    if request.method == 'POST':
        # Get the data from the forms (one form for user data and one form for user profile data)
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, instance=user_profile)

        # If both of the forms are valid
        if user_form.is_valid() and profile_form.is_valid():
            # Save the form data in the database
            user_form.save()
            profile = profile_form.save(commit=False)

            # If the user has submitted another photo, replace the current profile picture with that photo
            if 'profilePicture' in request.FILES:
                profile.profilePicture = request.FILES['profilePicture']

            # Save the data as final
            profile.save()

            # Redirect the user to the account page
            return redirect('eventastic:account')

    else:
        # Else if the form was not submitted then display the forms with the pre-existing information
        user_form = EditUserForm(request.POST or None, instance=request.user, initial={'first_name': request.user.first_name, 'last_name': request.user.last_name, 'email': request.user.email})
        profile_form = EditProfileForm(request.POST or None, instance=user_profile, initial={'DOB': user_profile.DOB, 'profilePicture': user_profile.profilePicture})

        # Store the forms in the context dictionary
        context_dict['user_form'] = user_form
        context_dict['profile_form'] = profile_form

        # Render the view onscreen using the given context
        return render(request, 'eventastic/edit_account.html', context=context_dict)

"""
This view renders the page and form that allows the user to delete their account onscreen
"""
@login_required
def delete_account(request):
    # Define empty context dictionary
    context_dict = {}

    # If the method is POST (form has been submitted) the form will be processed
    if request.method == 'POST':
        # Get the data from the form
        form = DeleteUserForm(request.POST)

        # Check the password is correct by authenticating the user
        user = authenticate(username=request.user, password=form.data['password'])

        # If the password is correct and the user is active
        if user:
            if user.is_active:
                # Gets the user object in the User table
                user_to_delete = User.objects.get(username=request.user)
                # Deletes the user object
                # This also deletes the user profile instance as the user field in UserProfile is set to CASCADE
                user_to_delete.delete()

                # Redirect the user to the home page
                return redirect('eventastic:index')

            else:
                # If the user account is disabled display error message
                messages.error(request, "Account is Disabled")

        else:
            # If the user does not exist (incorrect password) display an error message
            messages.error(request, "Invalid Form")
    else:
        # If the user has not submitted the form then create an empty form
        form = DeleteUserForm()

    # Store the form in the context dictionary
    context_dict['form'] = form

    # Render the view onscreen using the given context
    return render(request, 'eventastic/delete_account.html', context=context_dict)

"""
This view renders the page with Eventastic contact information onscreen
"""
def contact_us(request):
    # Render the view onscreen
    return render(request, 'eventastic/contact_us.html')


"""
This view is called when the user clicks the interest button and decides whether
to add interest or remove interest on the user's behalf
This view in combination with AJAX allows the number of users interested to
be updated without refreshing the page
"""
@login_required
def interest(request):
    # If the user has clicked the button
    if request.GET.get('action') == 'get':
        # Initialise the result aand set the name to the name of the current event
        result = ''
        name = request.GET.get('name')

        # Get the currently logged in user
        user_profile = UserProfile.objects.get(user=request.user.id)
        # Get the current event
        event = Event.objects.get(name=name)
        # If the user is already interested in attending the event (and they have clicked it again)
        if event.usersInterested.filter(user=user_profile).exists():
            # Remove them from the interested users
            event.usersInterested.remove(user_profile)
            # Decrease the number of interested users by 1
            event.numberInterested -= 1
            # Save the new number of interested
            result = event.numberInterested
            # Save the updated information
            event.save()
            # Set liked to False (user is now no longer interested)
            liked = False

        # If the user was not interested before clicking the button
        else:
            # Add them to the interested users
            event.usersInterested.add(user_profile)
            # Increase the number of interested users by 1
            event.numberInterested += 1
            # Save the new number of interested
            result = event.numberInterested
            # Save the updated information
            event.save()
            # Set liked to True (user is now interested)
            liked = True

        # Return the new number of users interested and a boolean value indicating if the user is interested
        # as a JSON response
        return JsonResponse({'result': result, 'liked': liked, })

"""
This view renders the page that displays all the users registered on Eventastic onscreen
"""
def find_users(request):
    # Define empty context dictionary
    context_dict = {}

    # Get all the users and order them alphabetically
    users = UserProfile.objects.order_by('user')
    # Store the users in the context dictionary
    context_dict['users'] = users

    # Render the view onscreen using the given context
    return render(request, 'eventastic/find_users.html', context=context_dict)

"""
This view renders all the events that a given user has organised onscreen
"""
def show_user_events(request, user_slug):
    # Define empty context dictionary
    context_dict = {}

    # Get the requested user using the user_slug (the user slug is just simply the username)
    requested_user = UserProfile.objects.get(user=user_slug)
    # get all the events the requested user has organised
    user_events = Event.objects.filter(createdBy=requested_user)

    # Store the events and the requested user in the context dictionary
    context_dict['user_events'] = user_events
    context_dict['requested_user'] = requested_user

    # Render the view onscreen using the given context
    return render(request, 'eventastic/show_user_events.html', context=context_dict)
