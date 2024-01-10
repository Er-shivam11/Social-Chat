from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, authenticate
from accounts.models import CustomUser
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.shortcuts import get_object_or_404, redirect
from accounts.models import UserRelationship  # Import the UserRelationship model

from .models import Post, Comment, Like

from .models import Post  # Import your Post model
from .forms import PostForm  , CommentForm# Import your PostForm

from django.http import JsonResponse

# Create your views here.
@login_required(login_url="login")
def home(request):
    return render(request,'home.html')

def messages(request):
    user_profile = CustomUser.objects.filter(username=request.user.username)
    user_list = CustomUser.objects.filter(~Q(username=request.user.username) & ~Q(is_superuser=True) & Q(is_active=True))

    if request.GET.get('search'):
        user_list = user_list.filter(first_name__icontains=request.GET.get('search'))

    context = {"userprofile": user_profile, "userlist": user_list}
    return render(request, 'auth/messages.html', context)

from django.shortcuts import render, redirect


def chatPage(request, *args, **kwargs):
	if not request.user.is_authenticated:
		return redirect("login-user")
	context = {}
	return render(request, "chatPage.html", context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.username
            post.save()
            return redirect('userhome')
    else:
        # Initialize the form with the 'user' field set to the currently logged-in user's username
        form = PostForm(initial={'user': request.user.username})

    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'createpost.html', {'form': form, 'posts': posts})

def edit_post(request, post_id):
    # Retrieve the post object to be edited
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')  # Replace 'home' with your homepage URL name
    else:
        form = PostForm(instance=post)

    posts = Post.objects.all().order_by('-created_at')
    
    return render(request, 'editpost.html', {'form': form, 'posts': posts})

def follow_user(request, user_id):
    # Get the user you want to follow
    user_to_follow = get_object_or_404(CustomUser, id=user_id)

    # Ensure that the user is not trying to follow themselves
    if request.user != user_to_follow:
        # Create a UserRelationship object representing the follow
        UserRelationship.objects.get_or_create(user=request.user, followed_user=user_to_follow)

    # Redirect to the user's profile or any other appropriate page
    return redirect('user_profile', user_id=user_id)

def unfollow_user(request, user_id):
    # Get the user you want to unfollow
    user_to_unfollow = get_object_or_404(CustomUser, id=user_id)

    # Delete the UserRelationship object representing the unfollow
    UserRelationship.objects.filter(user=request.user, followed_user=user_to_unfollow).delete()

    # Redirect to the user's profile or any other appropriate page
    return redirect('user_profile', user_id=user_id)


def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
            return redirect('userhome')  # Replace 'userhome' with your homepage URL name

    form = CommentForm()
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    return render(request, 'comment.html', {'form': form, 'comments': comments})

def toggle_like(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()

    like_count = post.likes.count()
    liked = created or not like.is_active  # Determine if the user liked or unliked the post

    return JsonResponse({'liked': liked, 'like_count': like_count})

