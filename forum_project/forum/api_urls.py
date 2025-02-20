from django.urls import path
from .views import (
    TopicListCreateView, TopicDetailView,
    PostListCreateView, PostDetailView,
    CommentListCreateView, CommentDetailView,
    EventListCreateView, EventDetailView,
    PollListCreateView, PollDetailView, vote,
    ResumeListCreateView
)

urlpatterns = [
    path('topics/', TopicListCreateView.as_view(), name='topic-list-create'),
    path('topics/<int:pk>/', TopicDetailView.as_view(), name='topic-detail'),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('polls/', PollListCreateView.as_view(), name='poll-list-create'),
    path('polls/<int:pk>/', PollDetailView.as_view(), name='poll-detail'),
    path('polls/vote/<int:option_id>/', vote, name='vote'),
    path('resumes/', ResumeListCreateView.as_view(), name='resume-list-create'),
]
