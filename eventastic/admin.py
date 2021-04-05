from django.contrib import admin

from eventastic.models import Category, UserProfile, Event, Comment


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class EventAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(Comment)
