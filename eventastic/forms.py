from django import forms
from eventastic.models import UserProfile, Category, Event
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    profilePicture = forms.ImageField(required=False)

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

class EventForm(forms.ModelForm):
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    name = forms.CharField(max_length=30)
    description = forms.CharField(max_length=200)
    start = forms.DateField(required=False)
    address = forms.CharField(max_length=50)
    postcode = forms.CharField(max_length=10)
    picture = forms.ImageField(required=False)
    averageRating = forms.DecimalField(widget=forms.HiddenInput(), initial=0)
    numberInterested = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    createdBy = forms.CharField(widget=forms.HiddenInput(), required=False)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Event
        fields = ('category', 'name', 'description', 'start', 'address', 'postcode', 'picture')
