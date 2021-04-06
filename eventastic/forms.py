from django import forms
from django.contrib.auth.models import User

from eventastic.models import UserProfile, Category, Event, Comment

# Forms used in the Eventastic Project
# All the form inputs are styled with the Bootstrap form control class as seen in the widgets

# Form to register a new User (this form takes in data associated with the User Table)
class UserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password',)

        help_texts = {
            'username': None
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    # Clean this data and raise an error if the two password fields do not match
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm password fields do not match"
            )

        elif len(password) < 8:
            raise forms.ValidationError(
                "password is too short"
            )

        elif (password.isdecimal()):
            raise forms.ValidationError(
                "password cannot only contain numbers"
            )


# Form to register a new User (this form takes in data associated with the UserProfile Table)
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('DOB', 'profilePicture')

        labels = {
            'DOB': 'Date of Birth',
            'profilePicture': 'Profile Picture'
        }

        widgets = {
            'DOB': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'YYYY-MM-DD', 'type': 'date'}),
            'profilePicture': forms.FileInput(attrs={'class': 'form-control'}),
        }

# Form to create a new category in the Eventastic web app
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


# Form to create a new event in the Eventastic web app
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('category', 'name', 'description', 'startDate', 'startTime', 'address', 'postcode', 'picture')

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'startDate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'startTime': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time', 'placeholder': 'hh-mm'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'postcode': forms.TextInput(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control'}),
        }


# Form to update details associated with the User Table
class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
        }


# Form to update details associated with the UserProfile Table
class EditProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('DOB', 'profilePicture',)

        widgets = {
            'DOB': forms.DateInput(attrs={'class': 'form-control'}),
            'profilePicture': forms.FileInput(attrs={'class': 'form-control'}),
        }


# Form to provide confirmation before deleting an account
class DeleteUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password',)

        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }


# Form to add a new comment to an existing event
class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('comment',)

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
