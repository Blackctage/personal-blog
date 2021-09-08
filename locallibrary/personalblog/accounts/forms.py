import re

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm, DateTimeInput, TextInput, Textarea, FileInput, URLInput, DateInput
from phonenumber_field.formfields import PhoneNumberField

from .models import Profile


class SignUpForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Ваше имя"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Новый пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Подтвердите пароль"}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Ваш email"}))

    class Meta(UserCreationForm.Meta):
        model = User
        # I've tried both of these 'fields' declaration, result is the same
        # fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

        fields = ('username', 'email', 'password1', 'password2')


class ProfileUpdateForm(ModelForm):
    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Profile
        fields = ['bio', 'avatar_photo', 'website', 'phone_number']

        widgets = {
            'bio': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'bio',
            }),
            'birth_date': DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'birth_date',
            }),
            'avatar_photo': FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'avatar_photo',
            }),
            'website': URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'website',
            })
        },


class UserForm(forms.ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Username or Email"}))

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', "placeholder": "Password"}))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "first name"}))
    last_name = forms.CharField(max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "last name"}))
    email = forms.EmailField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Ваш email"}))
    username = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Ваше имя"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

    def clean_username(self):
        username = self.cleaned_data['username']

        if not re.match(r'^[A-Za-z0-9_-]+$', username):
            raise forms.ValidationError("Usernames can only use letters, numbers, underscores and periods")
        return username


