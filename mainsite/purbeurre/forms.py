from django import forms
from django.contrib.auth.models import User


class MemberForm(forms.Form):
    """ This class creates a form to register a new member """

    username = forms.CharField(
        label="Nom d'utilisateur",
        min_length=2, max_length=30,
        widget=forms.TextInput,
        required=True,
    )
    email = forms.EmailField(
        label="Adresse Email",
        widget=forms.EmailInput,
        max_length=30,
        required=True
    )
    password = forms.CharField(
        label="Mot de passe",
        max_length=32,
        widget=forms.PasswordInput,
        required=True
    )


class ConnectionForm(forms.Form):
    """ This class creates a form to authenticate a user """

    email = forms.CharField(
        label="Adresse Email",
        widget=forms.TextInput
    )
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput
    )
    redirection = forms.CharField(
        widget=forms.HiddenInput,
        required=False
    )


class ChangePasswordForm(forms.Form):
    """ This class creates a form to change user's password """

    old_password = forms.CharField(
        label="Entrez l'ancien mot de passe",
        widget=forms.PasswordInput,
        required=True
    )
    new_password1 = forms.CharField(
        label="Entrez le Nouveau mot de passe",
        max_length=32,
        widget=forms.PasswordInput,
        required=True
    )
    new_password2 = forms.CharField(
        label="Retapez le Nouveau mot de passe",
        max_length=32,
        widget=forms.PasswordInput,
        required=True
    )
