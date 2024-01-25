from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from accounts.models import Profile


class LoginForm(AuthenticationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "password",
        ]

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Username",
                "required": "true",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "required": "true",
            }
        )
    )


class RegistrateForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ("username", "password1", "password2")
        widgets = {"username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Username"})}

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "New password"
            }
        )
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm password"
            }
        )
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("first_name", "last_name", "photo",)

        widgets = {
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control rounded border border-success p-2 mb-2",
                    "placeholder": "First name"
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control rounded border border-success p-2 mb-2",
                    "placeholder": "Last name"
                }
            ),
            "photo": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }
