from django import template
from eventastic.models import UserProfile, Event, Category

register = template.Library()

@register.inclusion_tag('eventastic/show_profile_pic.html')
def get_user_profile_pic(user_id):
    return {'user_profile': UserProfile.objects.get(user=user_id)}

@register.simple_tag
def get_recently_published_events():
    return Event.objects.order_by('-created')[:6]

@register.simple_tag
def get_top_categories():
    categories = []
    top_categories = []

    for category in Category.objects.all():
        total_events = len(Event.objects.filter(category=category))

        categories.append((category, total_events))

    categories.sort(key=lambda tup: tup[1], reverse=True)

    for category in categories:
        top_categories.append(category[0])

    return top_categories[:6]

@register.simple_tag
def get_top_organisers():
    organisers = []
    top_organisers = []

    for organiser in UserProfile.objects.all():
        total_events = len(Event.objects.filter(createdBy=organiser))

        organisers.append((organiser, total_events))

    organisers.sort(key=lambda tup: tup[1], reverse=True)

    for organiser in organisers:
        top_organisers.append(organiser[0])
        
    return top_organisers[:6]
