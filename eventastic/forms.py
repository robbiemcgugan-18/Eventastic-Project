from django import forms
from eventastic.models import UserProfile, Category, Event
from django.contrib.auth.models import User
from django.views.generic.edit import UpdateView

class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('DOB', 'profilePicture')

        widgets = {
            'DOB': forms.DateInput(attrs={'class': 'form-control'}),
            'profilePicture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name', 'description', 'picture')

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('category', 'name', 'description', 'start', 'address', 'postcode', 'picture')

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'start': forms.DateInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
        }

class EditUserForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('email',)

class EditProfileForm(forms.ModelForm):
    DOB = forms.DateField()
    profilePicture = forms.ImageField(required=True)

    class Meta:
        model = UserProfile
        fields = ('DOB','profilePicture',)

class DeleteUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password',)

        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
