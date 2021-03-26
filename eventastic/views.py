from django.shortcuts import render, redirect
from eventastic.forms import UserForm, UserProfileForm, CategoryForm, EventForm, EditUserForm, EditProfileForm, DeleteUserForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from eventastic.models import Category, Event, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

def index(request):

    return render(request, 'eventastic/index.html')

def register(request):
    # Initialises a variable that tracks if the user has registered an account
    registered = False

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

            if 'profilePicture' in request.FILES:
                profile.profilePicture = request.FILES['profilePicture']

            profile.save()

            # The user has now registered an account so registered is True
            registered = True

            new_user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))

            login(request, new_user)

            # Redirect the user to the home page
            return redirect(reverse('eventastic:index'))

        # If the form information is not valid then print the errors
        else:
            messages.error(request, "Form is invalid")

    # If the form has not been submitted display the form onscreen
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the view onscreen using the given context
    return render(request, 'eventastic/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
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

            # If the account exists but is disabled, notify user
            else:
                return HttpResponse("Your account is disabled")

        # If an account with the given details does not exist, notify the user
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied")

    # If the form has not been submitted, render the view onscreen
    else:
        return render(request, 'eventastic/login.html')


@login_required
def user_logout(request):
    # Log the user out
    logout(request)

    # Redirect the user back to the home page
    return redirect(reverse('eventastic:index'))

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

@login_required
def create_category(request):
    # Define the form that needs to be displayed onscreen
    form = CategoryForm()

    # If the method is POST (form has been submitted) the form will be processed
    if request.method == 'POST':
        # Get the data from the form
        form = CategoryForm(request.POST)

        print(request.FILES)

        # If the form information is valid then save the information in the database
        if form.is_valid():
            form_data = form.save(commit=False)

            if 'picture' in request.FILES:
                form_data.picture = request.FILES['picture']

            form_data.save()

            # Get the slug for the created category
            category_name_slug = form_data.slug
            # Redirect the user to the page for that category using the slug
            return redirect('eventastic:show_category', category_name_slug=category_name_slug)

        # If the form information is not valid display the errors
        else:
            print(form.errors)

    # If the form has not been submitted then render the view onscreen
    else:
        return render(request, 'eventastic/create_category.html', context={'form': form})

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

    # Render the view onscreen using the given context
    return render(request, 'eventastic/show_event.html', context=context_dict)

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

            form_data.save()

            # Ge the slug for the created event
            event_name_slug = form_data.slug

            # Get the slug for the category the created event comes under
            category_obj = Category.objects.get(name=form_data.category)
            category_name_slug = category_obj.slug

            # Redirect the user to th epage that shows the event using the two slugs
            return redirect('eventastic:show_event', category_name_slug=category_name_slug, event_name_slug=event_name_slug)

        # If the form information is not valid then print the errors
        else:
            print(form.errors)

    # If the form has not been submitted then render the view onscreen
    else:
        return render(request, 'eventastic/create_event.html', context={'form': form})

def categories(request):
    # Define empty context dictionary
    context_dict = {}

    # Order the categories by name (A-Z) and store them in the context dictionary
    categories = Category.objects.order_by('name')
    context_dict['categories'] = categories

    # Render the view onscreen using the given context
    return render(request, 'eventastic/categories.html', context=context_dict)

def account(request):
    context_dict = {}

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('eventastic:account')

        else:
            messages.error(request, "Form is invalid")

    else:
        form = PasswordChangeForm(request.user)

    context_dict['form'] = form

    user_profile = UserProfile.objects.get(user=request.user.id)
    organised_events = Event.objects.filter(createdBy=user_profile)

    context_dict['user_profile'] = user_profile
    context_dict['organised_events'] = organised_events

    return render(request, 'eventastic/account.html', context=context_dict)

def edit_account(request):
    context_dict = {}
    user_profile = UserProfile.objects.get(user=request.user.id)

    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, instance=user_profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)

            if 'profilePicture' in request.FILES:
                profile.profilePicture = request.FILES['profilePicture']

            profile.save()

            return redirect('eventastic:account')

    else:
        user_form = EditUserForm(request.POST or None, instance=request.user, initial={'email': request.user.email})
        profile_form = EditProfileForm(request.POST or None, instance=user_profile, initial={'DOB': user_profile.DOB, 'profilePicture': user_profile.profilePicture})

        context_dict['user_form'] = user_form
        context_dict['profile_form'] = profile_form

        return render(request, 'eventastic/edit_account.html', context=context_dict)

def delete_account(request):
    context_dict = {}

    if request.method == 'POST':
        form = DeleteUserForm(request.POST)

        user = authenticate(username=request.user, password=form.data['password'])

        if user:
            if user.is_active:
                user_to_delete = User.objects.get(username=request.user)
                user_to_delete.delete()

                return redirect('eventastic:index')

            else:
                messages.error(request, "Account is Disabled")

        else:
            messages.error(request, "Invalid Form")
    else:
        form = DeleteUserForm(request.POST)


    context_dict['form'] = form

    return render(request, 'eventastic/delete_account.html', context=context_dict)
