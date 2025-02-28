# forum/forms.py

from django import forms
from .models import User, Event, Post, Comment, Poll, Resume

class CustomUserCreationForm(forms.ModelForm):
    # Add the fields you need in the form
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password']  # Add 'name' and 'email'

    # Optional: You can add custom validation here for email or other fields
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already taken')
        return email

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        return password_confirm


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["title", "description", "date"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["topic", "title", "content"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["post", "content", "author"]

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ["question"]

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ["name", "email", "resume_file"]
