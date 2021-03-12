from django.contrib import admin
from eventastic.models import Category, UserProfile, Event, Attend, Comment

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(Attend)
admin.site.register(Comment)
