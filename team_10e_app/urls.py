from django.urls import path
from team_10e_app import views

app_name = 'team_10e_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name="login"),
    path('logout/', views.user_logout, name='logout'),
]