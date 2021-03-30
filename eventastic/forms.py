from django import forms
from django.contrib.auth.models import User

from eventastic.models import UserProfile, Category, Event, Comment


class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
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
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('category', 'name', 'description', 'start', 'address', 'postcode', 'picture')

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'start': forms.DateInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


class EditUserForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }


class EditProfileForm(forms.ModelForm):
    DOB = forms.DateField()
    profilePicture = forms.ImageField()

    class Meta:
        model = UserProfile
        fields = ('DOB', 'profilePicture',)

        widgets = {
            'DOB': forms.DateInput(attrs={'class': 'form-control'}),
            'profilePicture': forms.FileInput(attrs={'class': 'form-control'}),
        }


class DeleteUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password',)

        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
