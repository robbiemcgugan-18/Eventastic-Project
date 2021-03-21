from django import template
from eventastic.models import UserProfile

register = template.Library()

@register.inclusion_tag('eventastic/show_profile_pic.html')
def get_user_profile_pic(user_id):
    return {'user_profile': UserProfile.objects.get(user=user_id)}
