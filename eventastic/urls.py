from django.urls import path
from eventastic import views

app_name = 'eventastic'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name='logout'),
    path('category/<slug:category_name_slug>/', views.show_category, name='show_category'),
    path('category/create-category', views.create_category, name='create_category'),
]
