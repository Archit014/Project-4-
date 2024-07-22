import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from .models import User, Post, Like, Followers


def index(request):
    if request.user.is_authenticated:
        likes = Like.objects.filter(user = request.user)
        liked_post = []
        for like in likes:
            liked_post.append(like.post)
    else:
        liked_post = []
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html",{
        "posts":page_obj,
        "liked_post":liked_post
    })

@login_required
def profile(request, name):
    if request.method == "POST":
        follows = Followers.objects.filter(user = request.user)
        count = 0
        for follow in follows:
            if follow.followers.username == name:
                follow.delete()
                count = 1
        if count == 0:
            user = User.objects.get(username = name)
            new = Followers(user = request.user, followers = user)
            new.save()
        return HttpResponseRedirect(reverse("following"))
    
    likes = Like.objects.filter(user = request.user)
    liked_post = []
    for like in likes:
        liked_post.append(like.post)
    user = User.objects.get(username = name)
    posts = Post.objects.filter(user = user.id).order_by('-timestamp')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    followers = Followers.objects.filter(followers = user.id).count()
    following = Followers.objects.filter(user = user.id).count()
    follows = Followers.objects.filter(user = request.user)
    action = "follow"
    for follow in follows:
        if follow.followers.username == name:
            action = 'unfollow'
    return render(request, "network/profile.html",{
        "name":name,
        "posts":page_obj,
        "followers":followers,
        "following":following,
        "action":action,
        "username":request.user.username,
        "liked_post":liked_post
    })

@login_required
def following(request):
    followers = Followers.objects.filter(user = request.user)
    follow = []
    for follower in followers:
        follow.append(follower.followers)
    
    likes = Like.objects.filter(user = request.user)
    liked_post = []
    for like in likes:
        liked_post.append(like.post)
    posts = Post.objects.filter(user__in = follow).order_by('-timestamp')
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html",{
        "posts":page_obj,
        "liked_post":liked_post
    })

@login_required
def new(request):
    if request.method == "POST":
        content = request.POST["content"]

        post = Post(
        user=request.user,
        content=content
        )
        post.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "network/new.html")

    

@csrf_exempt
@login_required
def like(request, id):

    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    
    # Get contents of post
    react = data.get("post", "")
    if not react:
        return render(request, "network/index.html")
    post = Post.objects.get(pk = id)
    if react == "like":
        like = Like(
            user=request.user,
            post=post
        )
        like.save()
    if react == "unlike":
        like = Like.objects.filter(user=request.user, post = post)
        like.delete()

    return JsonResponse({"message": "post reacted."}, status=201)

@csrf_exempt
@login_required
def edit(request, id):

    
    # Composing a new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    
    # Get contents of post
    content = data.get("content", "")
    if not content:
        return render(request, "network/index.html")

    post = Post.objects.get(pk = id)
    post.content = content
    post.save()

    return JsonResponse({"message": "post edited."}, status=201)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
