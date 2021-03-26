from django.urls import path
from eventastic import views

app_name = 'eventastic'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name="login"),
    path('contact-us/', views.contact_us, name="contact_us"),
    path('login/account/', views.account, name='account'),
    path('login/account/edit/', views.edit_account, name='edit_account'),
    path('login/account/delete/', views.delete_account, name='delete_account'),
    path('logout/', views.user_logout, name='logout'),
    path('categories/', views.categories, name='categories'),
    path('categories/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('categories/create-category', views.create_category, name='create_category'),
    path('create_event/', views.create_event, name='create_event'),
    path('categories/<slug:category_name_slug>/<slug:event_name_slug>/', views.show_event, name='show_event'),
]
