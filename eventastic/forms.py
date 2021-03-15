from django import forms
from eventastic.models import UserProfile, Category
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('DOB', 'profilePicture')

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=30)
    description = forms.CharField(max_length=200)
    picture = forms.ImageField(required=False)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name', 'description', 'picture')
