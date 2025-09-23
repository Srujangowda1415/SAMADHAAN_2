from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm  # Make sure you have created this form in forms.py
from .models import Post, Bid
from .forms import PostForm
from django.shortcuts import get_object_or_404



# Create your views here.
def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def home(request):
    posts = Post.objects.all().order_by('-created_at')

    return render(request, 'home.html', {'posts': posts})

@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html',{'form': form})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:  # Only allow author to delete
        post.delete()
    return redirect('home')

def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return redirect('home')  # Only allow author to update

    if request.method == "POST":
        post.title = request.POST.get("title")
        post.content = request.POST.get("content")
        post.save()
        return redirect("home")
    else:
        form = PostForm(instance=post)
        
    return render(request, 'create_post.html', {'form': form})

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)   # Unlike
    else:
        post.likes.add(request.user)      # Like
    return redirect('home')  # Redirect back to home or post detail

    
def signup_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {'form': form})

# ---------------------------
# Contractor Views (new)
# ---------------------------
@login_required(login_url='login')
def contractor_dashboard(request):
    # TODO: If you add user roles, restrict access here:
    # if request.user.profile.role != "contractor":
    #     return redirect("home")

    posts = Post.objects.all().order_by("-created_at")
    return render(request, "contractor_dashboard.html", {"posts": posts})


# @login_required(login_url='login')
# def place_bid(request, post_id):
#     # TODO: If you add user roles, restrict access here:
#     # if request.user.profile.role != "contractor":
#     #     return redirect("home")

#     post = get_object_or_404(Post, id=post_id)

#     if request.method == "POST":
#         amount = request.POST.get("amount")
#         proposal = request.POST.get("proposal")

#         Bid.objects.create(
#             post=post,
#             contractor=request.user,
#             amount=amount,
#             proposal=proposal
#         )
#         return redirect("contractor_dashboard")

#     return render(request, "place_bid.html", {"post": post})

@login_required(login_url='login')
def place_bid(request, post_id):
    # if request.user.profile.role != "contractor":
    #     return redirect("home")

    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        amount = request.POST.get("amount")
        proposal = request.POST.get("proposal")

        Bid.objects.create(
            post=post,
            contractor=request.user,
            amount=amount,
            proposal=proposal
        )
        return redirect("contractor_dashboard")

    return render(request, "place_bid.html", {"post": post})
