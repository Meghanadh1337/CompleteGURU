from rest_framework import generics
from .models import Topic , Post , Comment ,Event , Poll , PollOption ,Resume
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TopicSerializer , PostSerializer , CommentSerializer , EventSerializer , PollSerializer ,ResumeSerializer
from django.shortcuts import render , get_object_or_404
from django.http import JsonResponse
from django.contrib.auth import login , get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

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

def resume_review(request):
    if request.method == "POST":
        print("POST request received")  # Debugging step
        if "resume_file" in request.FILES:
            uploaded_file = request.FILES["resume_file"]
            print(f"File received: {uploaded_file.name}")  # Debugging step

            resume = Resume.objects.create(resume_file=uploaded_file, reviewer="Pending")
            print(f"File saved at: {resume.resume_file.path}")  # Debugging step
        else:
            print("No file in request.FILES")  # Debugging step

    resumes = Resume.objects.all()
    return render(request, "resume_review.html", {"resumes": resumes})

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

# Login view
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home after login
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})



