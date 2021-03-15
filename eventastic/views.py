from django.shortcuts import render, redirect
from eventastic.forms import UserForm, UserProfileForm, CategoryForm, EventForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from eventastic.models import Category, Event, UserProfile
from django.contrib.auth.models import User

def index(request):

    return render(request, 'eventastic/index.html')

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.profilePicture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()


    return render(request, 'eventastic/register.html', context = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('eventastic:index'))

            else:
                return HttpResponse("Your account is disabled")

        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied")

    else:
        return render(request, 'eventastic/login.html')


@login_required
def user_logout(request):
    logout(request)

    return redirect(reverse('eventastic:index'))

def show_category(request, category_name_slug):

    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)

        events = Event.objects.filter(category=category)

        context_dict['events'] = events
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['events'] = None

    return render(request, 'eventastic/show_category.html', context=context_dict)

@login_required
def create_category(request):

    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form_data = form.save(commit=True)

            category_name_slug = form_data.slug
            return redirect('eventastic:show_category', category_name_slug=category_name_slug)

        else:
            print(form.errors)

    else:
        return render(request, 'eventastic/create_category.html', context={'form': form})

def show_event(request, category_name_slug, event_name_slug):

    context_dict = {}

    try:
        event = Event.objects.get(slug=event_name_slug)

        context_dict['event'] = event

    except Event.DoesNotExist:
        context_dict['event'] = None

    return render(request, 'eventastic/show_event.html', context=context_dict)

@login_required
def create_event(request):

    form = EventForm()

    if request.method == 'POST':
        form = EventForm(request.POST)

        if form.is_valid():
            form.instance.createdBy = UserProfile.objects.get(user=request.user)

            form_data = form.save(commit=True)

            event_name_slug = form_data.slug

            category_obj = Category.objects.get(name=form_data.category)
            category_name_slug = category_obj.slug

            return redirect('eventastic:show_event', category_name_slug=category_name_slug, event_name_slug=event_name_slug)

        else:
            print(form.errors)

    else:
        return render(request, 'eventastic/create_event.html', context={'form': form})

def categories(request):

    context_dict = {}

    categories = Category.objects.order_by('name')

    context_dict['categories'] = categories

    return render(request, 'eventastic/categories.html', context=context_dict)
