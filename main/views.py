from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Follow
from .forms import PostForm, UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

@login_required
def home(request):
    # show posts from following + self
    following_ids = request.user.following_set.values_list('following_id', flat=True)
    posts = Post.objects.filter(author__in=list(following_ids) + [request.user.id]).order_by('-created_at')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'main/home.html', {'posts': posts, 'form': form})

def profile(request, username):
    user_obj = get_object_or_404(User, username=username)
    posts = user_obj.posts.all().order_by('-created_at')
    is_following = request.user.is_authenticated and Follow.objects.filter(
        follower=request.user, following=user_obj
    ).exists()

    return render(request, 'main/profile.html', {
        'profile_user': user_obj,
        'posts': posts,
        'is_following': is_following
    })

@login_required
def follow_toggle(request, username):
    target = get_object_or_404(User, username=username)
    if target != request.user:
        relation, created = Follow.objects.get_or_create(
            follower=request.user, following=target
        )
        if not created:
            relation.delete()

    return redirect('profile', username=target.username)

@login_required
def like_toggle(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(request.META.get("HTTP_REFERER", "/"))
