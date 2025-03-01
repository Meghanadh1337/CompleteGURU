# forum/forms.py

from django import forms
from .models import User, Event, Post, Comment, Poll, Resume

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'password']

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        print("confirmed")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()
        print("saved user")
        return user

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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Hash the password
        if commit:
            user.save()
        return user

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
