from django.contrib import admin
from eventastic.models import Category, UserProfile, Event, Attend, Comment

admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(Attend)
admin.site.register(Comment)
