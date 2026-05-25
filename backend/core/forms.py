"""
core/forms.py — Django Forms

All user-input validation lives here.
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
    email    = forms.EmailField(max_length=254)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)

    def __init__(self, *args, request=None, **kwargs):
        self._request = request
        self._user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cd = super().clean()
        email = cd.get('email', '').strip().lower()
        pw    = cd.get('password', '')
        if email and pw:
            self._user = authenticate(self._request, username=email, password=pw)
            if self._user is None:
                raise forms.ValidationError('Invalid email or password.')
        return cd

    def get_user(self):
        return self._user


class SignupForm(forms.Form):
    email    = forms.EmailField(max_length=254)
    password = forms.CharField(min_length=6, widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def save(self):
        e = self.cleaned_data['email']
        p = self.cleaned_data['password']
        return User.objects.create_user(username=e, email=e, password=p)


class AnalyzeForm(forms.Form):
    topic = forms.CharField(max_length=255, min_length=1)

    def clean_topic(self):
        return self.cleaned_data['topic'].strip()


class SaveIdeaForm(forms.Form):
    topic      = forms.CharField(max_length=255, required=False)
    idea_type  = forms.CharField(max_length=100, required=False)
    idea_title = forms.CharField(max_length=500)
    difficulty = forms.CharField(max_length=20, required=False)
    potential  = forms.CharField(max_length=20, required=False)
