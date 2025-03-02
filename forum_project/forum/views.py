from rest_framework import generics
from .models import Topic , Post , Comment ,Event , Poll , PollOption ,Resume
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TopicSerializer , PostSerializer , CommentSerializer , EventSerializer , PollSerializer ,ResumeSerializer
from django.shortcuts import render , get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import login , get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, EventForm, PostForm, CommentForm, PollForm, ResumeForm, UserProfileForm
from django.forms import modelform_factory
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
import json
from django.urls import reverse
import os
from .models import Resume, ImprovementArea, ResumeImprovement, ResumeVote

class TopicListCreateView(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class TopicDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  # Set author as the logged-in user

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class PollListCreateView(generics.ListCreateAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

class PollDetailView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

@api_view(["POST"])
def vote(request, option_id):  # Handles voting
    try:
        option = PollOption.objects.get(id=option_id)
        option.votes += 1
        option.save()
        return Response({"message": "Vote recorded!", "votes": option.votes})
    except PollOption.DoesNotExist:
        return Response({"error": "Option not found"}, status=404)

class ResumeListCreateView(generics.ListCreateAPIView):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer

@login_required
def home(request):
    return render(request, "home.html")

def events(request):
    event_list = Event.objects.all()  # Fetch all events
    return render(request, "events.html", {"events": event_list})

def event_list(request):
    events = Event.objects.all().values('id', 'title', 'description', 'date')
    return JsonResponse(list(events), safe=False)

def polls(request):
    poll_list = Poll.objects.all()  # Fetch all polls
    return render(request, "polls.html", {"polls": poll_list})

@login_required
def resume_review(request):
    resumes = Resume.objects.all().order_by('-uploaded_at')
    return render(request, 'resume_review.html', {'resumes': resumes})

@login_required
def upload_resume(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        resume_file = request.FILES.get('resume_file')

        if name and email and resume_file:
            resume = Resume.objects.create(
                name=name,
                email=email,
                resume_file=resume_file
            )

            # Check if improvement areas exist and create some if they don't
            improvement_areas = ImprovementArea.objects.all()
            if not improvement_areas.exists():
                # Create default improvement areas if none exist
                default_areas = [
                    {
                        'name': 'Resume Length',
                        'description': 'The resume is too long and should be condensed to highlight key information.',
                    },
                    {
                        'name': 'Formatting',
                        'description': 'The resume formatting could be improved for better readability and visual appeal.',
                    },
                    {
                        'name': 'Skills Section',
                        'description': 'The skills section needs more relevant skills or better organization.',
                    },
                    {
                        'name': 'Experience Details',
                        'description': 'Work experiences should be more achievement-oriented rather than task-based.',
                    },
                    {
                        'name': 'Education Section',
                        'description': 'Education information could be improved or reorganized.',
                    },
                ]

                for area_data in default_areas:
                    area = ImprovementArea.objects.create(
                        name=area_data['name'],
                        description=area_data['description']
                    )
                    ResumeImprovement.objects.create(resume=resume, area=area)
            else:
                # Use existing improvement areas
                for area in improvement_areas:
                    ResumeImprovement.objects.create(resume=resume, area=area)

            messages.success(request, "Resume uploaded successfully!")
            return redirect('view_resume', resume_id=resume.id)
        else:
            messages.error(request, "Please fill all required fields.")

    return redirect('resume_review')

@login_required
def view_resume(request, resume_id):
    resume = get_object_or_404(Resume, id=resume_id)
    improvements = ResumeImprovement.objects.filter(resume=resume).select_related('area')

    # Get areas the current user has voted on for this resume
    user_voted = ResumeVote.objects.filter(
        user=request.user,
        improvement__resume=resume
    ).values_list('improvement__area__id', flat=True)

    context = {
        'resume': resume,
        'improvements': improvements,
        'user_voted': user_voted,
    }

    return render(request, 'view_resume.html', context)

@login_required
def vote_resume(request, resume_id):
    if request.method == 'POST':
        resume = get_object_or_404(Resume, id=resume_id)
        area_id = request.POST.get('area_id')

        if area_id:
            try:
                improvement = ResumeImprovement.objects.get(resume=resume, area_id=area_id)

                # Check if user already voted for this improvement area
                vote_exists = ResumeVote.objects.filter(
                    user=request.user,
                    improvement=improvement
                ).exists()

                if not vote_exists:
                    # Create a vote record and increment the vote count
                    ResumeVote.objects.create(user=request.user, improvement=improvement)
                    improvement.votes += 1
                    improvement.save()
                    messages.success(request, "Your vote has been recorded.")
                else:
                    messages.info(request, "You have already voted for this improvement area.")
            except ResumeImprovement.DoesNotExist:
                messages.error(request, "Invalid improvement area.")
        else:
            messages.error(request, "No improvement area selected.")

    return redirect('view_resume', resume_id=resume_id)

def posts(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        comment_content = request.POST.get("comment_content")
        if post_id and comment_content:
            post = Post.objects.get(id=post_id)
            Comment.objects.create(post=post, content=comment_content, author=request.user)

    post_list = Post.objects.prefetch_related('comments').all()
    return render(request, "posts.html", {"posts": post_list})

def polls(request):
    if request.method == "POST":
        option_id = request.POST.get("option_id")
        if option_id:
            option = get_object_or_404(PollOption, id=option_id)
            option.votes += 1
            option.save()

    poll_list = Poll.objects.prefetch_related('options').all()
    return render(request, "polls.html", {"polls": poll_list})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})

def login_view(request):
    print("DEBUG: login_view executed")
    if request.method == "POST":
        print("DEBUG: Login POST request received")
        print("DEBUG: Received username:", request.POST.get("username"))
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            print("DEBUG: Authentication successful for user:", user)
            login(request, user)
            return redirect('home')
        else:
            print("DEBUG: Authentication failed - Errors:", form.errors)

    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})



MODEL_MAP = {
    "topic": Topic,
    "post": Post,
    "comment": Comment,
    "event": Event,
    "poll": Poll,
    "polloption": PollOption,
    "resume": Resume,
}

def handle_form(request, model_name, object_id=None):
    model = MODEL_MAP.get(model_name.lower())
    if not model:
        return render(request, "404.html", {"message": "Invalid Model"})

    FormClass = modelform_factory(model, exclude=[])
    instance = get_object_or_404(model, id=object_id) if object_id else None

    if request.method == "POST":
        form = FormClass(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect("manage_content")
    else:
        form = FormClass(instance=instance)

    return render(request, "add_object.html", {"form": form, "model_name": model_name})


def manage_content(request):
    User = get_user_model()
    users = User.objects.all()
    return render(request, "manage_content.html", {"users": users})

def delete_object(request, model_name, object_id):
    model_map = {
        "topic": Topic,
        "post": Post,
        "comment": Comment,
        "event": Event,
        "poll": Poll,
        "polloption": PollOption,
        "resume": Resume,
    }

    model = model_map.get(model_name.lower())
    if not model:
        messages.error(request, "Invalid model name.")
        return redirect("manage_content")

    obj = get_object_or_404(model, id=object_id)
    obj.delete()
    messages.success(request, f"{model_name.capitalize()} deleted successfully.")

    return redirect("manage_content")


@csrf_exempt
def update_permissions(request, user_id):
    from .models import User
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            user = User.objects.get(id=user_id)
            user.is_staff = data.get("is_staff", user.is_staff)
            user.is_superuser = data.get("is_superuser", user.is_superuser)
            user.save()
            return JsonResponse({"message": "Permissions updated successfully!"})
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def check_admin_status(request):
    """Returns JSON response indicating if the user is an admin."""
    return JsonResponse({"is_admin": request.user.is_staff or request.user.is_superuser})

def serve_resume_file(request, resume_id):
    """Serve resume file with appropriate content-type headers"""
    resume = get_object_or_404(Resume, id=resume_id)

    # Determine the content type based on file extension
    file_path = resume.resume_file.path
    content_type = "application/pdf"  # Default to PDF

    if file_path.endswith('.docx'):
        content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif file_path.endswith('.doc'):
        content_type = "application/msword"

    # Read file content
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=content_type)

    # Set content disposition header to inline to display in browser
    response['Content-Disposition'] = f'inline; filename="{resume.name}_resume{os.path.splitext(file_path)[1]}"'

    # Add header to allow embedding in iframe
    response['X-Frame-Options'] = 'SAMEORIGIN'

    return response


@login_required
def user_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        print("Form submitted")
        if form.is_valid():
            print("Form is valid")
            form.save()
            return redirect('user_profile')
        else:
            print("Form is not valid")
            print(form.errors)  # Print form errors for debugging
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'user_profile.html', {'user': user, 'form': form})