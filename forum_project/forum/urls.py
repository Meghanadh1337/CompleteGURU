from django.urls import path
from .views import home, polls, resume_review , posts ,event_list , register , login_view , manage_content , handle_form , delete_object, update_permissions, check_admin_status, upload_resume, view_resume, vote_resume, serve_resume_file
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
    path("manage/", manage_content, name="manage_content"),
    path("<str:model_name>/add/", handle_form, name="add_object"),
    path("<str:model_name>/edit/<int:object_id>/", handle_form, name="edit_object"),
    path("<str:model_name>/delete/<int:object_id>/", delete_object, name="delete_object"),
    path('update-permissions/<int:user_id>/', update_permissions, name='update_permissions'),
    path("check-admin-status/", check_admin_status, name="check_admin_status"),
    path('logout/', LogoutView.as_view(), name='logout'),  # Keep logout
    path('resume_review/', resume_review, name='resume_review'),
    path('resume/upload/', upload_resume, name='upload_resume'),
    path('resume/view/<int:resume_id>/', view_resume, name='view_resume'),
    path('resume/vote/<int:resume_id>/', vote_resume, name='vote_resume'),
    path('resume/file/<int:resume_id>/', serve_resume_file, name='serve_resume_file'),
]
