from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class User(AbstractUser):  # Extends Django's built-in User model
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "email"  # This tells Django to use email instead of username
    REQUIRED_FIELDS = ["username"]  # Username is still required

    def __str__(self):
        return self.email  # Change this to display email instead of username

# Create your models here.
class Topic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)  # Links post to a topic
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="comments")  # Links comment to a post
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Allow null authors



    def __str__(self):
        return self.content[:50]  # Show first 50 characters

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateTimeField()

    def __str__(self):
        return self.title

class Poll(models.Model):
    question = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="options")  # Links to Poll
    option_text = models.CharField(max_length=255)
    votes = models.IntegerField(default=0)  # Tracks vote count

    def __str__(self):
        return self.option_text

class Resume(models.Model):
    name = models.CharField(max_length=255)  # User's name
    email = models.EmailField()  # Contact email
    resume_file = models.FileField(upload_to="resumes/")  # Uploaded resume
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Upload timestamp
    reviewer = models.CharField(max_length=100, default="Pending")

    def __str__(self):
        return self.name
