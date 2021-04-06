from django import template
from eventastic.models import UserProfile, Event, Category

register = template.Library()

"""
Returns the user_profile of the currently logged in user
so the profile picture can be displayed using show_profile_pic.html
"""
@register.inclusion_tag('eventastic/show_profile_pic.html')
def get_user_profile_pic(user_id):
    return {'user_profile': UserProfile.objects.get(user=user_id)}

"""
Get the top most recenetly published events
by sorting the created field descending
"""
@register.simple_tag
def get_recently_published_events():
    return Event.objects.order_by('-created')[:6]

"""
Get the 6 categories with the most events in them
"""
@register.simple_tag
def get_top_categories():
    categories = []
    top_categories = []

    # Go through each category and find the total events in each category
    for category in Category.objects.all():
        total_events = len(Event.objects.filter(category=category))

        # Add the category and event total to a list
        categories.append((category, total_events))

    # Sort the list by the total_events tuple field (tup[1]) and reverse the list (highest to lowest)
    categories.sort(key=lambda tup: tup[1], reverse=True)

    # Get a list of only the categories i.e. remove the total_events field
    for category in categories:
        top_categories.append(category[0])

    # Return the top 6 categories
    return top_categories[:6]

"""
Get the 6 organisers who have organised the most events
"""
@register.simple_tag
def get_top_organisers():
    organisers = []
    top_organisers = []

    # Go through each user and find the total events each user has organised
    for organiser in UserProfile.objects.all():
        total_events = len(Event.objects.filter(createdBy=organiser))

        # Add the user and event total to a list
        organisers.append((organiser, total_events))

    # Sort the list by the total_events tuple field (tup[1]) and reverse the list (highest to lowest)
    organisers.sort(key=lambda tup: tup[1], reverse=True)

    # Get a list of only the users i.e. remove the total_events field
    for organiser in organisers:
        top_organisers.append(organiser[0])

    # Return the top 6 organisers
    return top_organisers[:6]
