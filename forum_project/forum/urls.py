from django.urls import path
from .views import home, polls, resume_review , posts ,event_list , register , login_view
from django.shortcuts import render
from django.contrib.auth.views import LogoutView

def event_page(request):
    return render(request, 'events.html')

urlpatterns = [
    path('', home, name='home'),
    path('polls/', polls, name='polls'),
    path('resume-review/', resume_review, name='resume-review'),
    path('posts/', posts, name='post-list'),
    path('events/data/', event_list, name='event_list_api'),
    path('events/', event_page, name='event_page') ,
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
]
