from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import  redirect
from django.shortcuts import get_object_or_404, redirect, render
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.forms import ModelForm
from django.core.paginator import Paginator
from django import forms
from .models import User, Post, Follow
import json



class PostForm(ModelForm):
    class Meta:
        model=Post
        fields=["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",      
                    "rows": 4}
            )
        }
      
        
        
        
      
def index(request):
    """Main page view. 
    Displays all posts in reverse chronological order (newest first), with pagination (10 posts per page).
    Also allows authenticated users to create new posts. """
    
    # Get all posts ordered by newest first
    posts_list = Post.objects.all().order_by("-timestamp") 
    
    # Paginate posts (10 per page)
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    
    
    # Handle new post submission
    if request.method=="POST":
            if request.user.is_authenticated:
                form=PostForm(request.POST)
                if form.is_valid():
                    post=form.save(commit=False)
                    post.user=request.user
                    post.save()
                    return HttpResponseRedirect(reverse("index"))
                
         # If user not logged in, redirect to login page
            else:
                return render(request, "network/login.html")

    else:
        form=PostForm()
        

    # Render index page with form and posts  
    return render(request, "network/index.html",{
                "form":PostForm(),
                "posts":posts
            })
        
        
        
        
def profile(request, username):
    """Profile page view.
    Displays:
        - The user's profile info
        - All posts made by that user (paginated)
        - Number of followers and following
        - Follow/Unfollow button for authenticated users
    """ 
    
    # Get the user whose profile we are viewing
    profile_user = get_object_or_404(User, username=username)
    
    # Get all posts from this user (newest first)
    posts_list = Post.objects.filter(user=profile_user).order_by("-timestamp") 
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    
    
    # Count followers and following
    followstatus = False
    followingNumber=Follow.objects.filter(follower=profile_user, followStatus=True).count()      
    followerNumber=Follow.objects.filter(following=profile_user, followStatus=True).count()
    
    
    # Check if the current logged-in user already follows this profile
    if request.user.is_authenticated:
        relation = Follow.objects.filter(
            follower=request.user,
            following=profile_user,
            followStatus=True
        ).first()
        if relation:
            followstatus = True



    # Render profile page
    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "followstatus": followstatus,
        "form":PostForm(),
        "posts":posts,
        "followerNumber":  followerNumber,
        "followingNumber":followingNumber, 
    })




@login_required
def following(request):
    """Following page view.
    Displays posts from all users that the current user follows.
    Includes pagination (10 posts per page).
    Accessible only to logged-in users."""
    
    
    # Get all users that the current user follows 
    following_users = [f.following for f in Follow.objects.filter(follower=request.user, followStatus=True)]
    posts_list = Post.objects.filter(user__in=following_users).order_by("-timestamp") 
    
    
    # Paginate posts (10 per page)
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get("page")
    posts = paginator.get_page(page_number)
    
    
    # Render the page
    return render(request, "network/following.html", {
        "posts": posts
    })
    
    
    
    
def followUser(request, username):
    """ Handles the follow/unfollow action.
    Only accessible via POST requests and by authenticated users. """
    
    # Ensure it's a POST request
    if request.user.is_authenticated and request.method == "POST":
        
        # Get the profile user to be followed/unfollowed
        profile_user = User.objects.get(username=username)
        
        # Get the requested action from the POST data
        action = request.POST.get("action")


        # Get or create a follow relationship between current user and profile user
        follow_obj, created = Follow.objects.get_or_create(
            follower=request.user,
            following=profile_user
        )
        
        
        # Update follow status based on action
        if action == "follow":
            follow_obj.followStatus = True
        elif action == "unfollow":
            follow_obj.followStatus = False

        # Save the relationship
        follow_obj.save()


        # Redirect back to the profile page
        return redirect("profile", username=profile_user.username)
    
    


    
def showFollowers(request, username):
    """Displays all users who follow the given profile user."""
    
    # Get the profile user
    profile_user = get_object_or_404(User, username=username)
    
    # Get all Follow objects where this user is being followed
    follows = Follow.objects.filter(following=profile_user, followStatus=True)
    follower_users = []

    for f in follows:
        follower_users.append(f.follower.username)


    # Render the followers page
    return render(request, "network/showFollowers.html", {
        "profile_user": profile_user,
        "follower_users": follower_users
    })
    
    
    
def showFollowing(request, username):
    """Displays all users that the given profile user is following."""
    
    # Get the profile user
    profile_user = get_object_or_404(User, username=username)
    
    # Get all Follow objects where this user is the follower
    follows = Follow.objects.filter(follower=profile_user, followStatus=True)
    
    following_users = []
    for f in follows:
        following_users.append(f.following.username)


    # Render the following pag
    return render(request, "network/showFollowing.html", {
        "profile_user": profile_user,
        "following_users": following_users
    })
        
        
        
@login_required       
def like_post(request, post_id):
    """Handles the like/unlike functionality for a post.
    This view is designed to be used with JavaScript (AJAX) requests."""
    
    # Check if method is POST
    if request.method == "POST":
        user=request.user       
        post = Post.objects.get(id=post_id)


        # Toggle like status
        if user in post.likes.all():
            post.likes.remove(user)
            liked=False
        else:
            post.likes.add(user)
            liked=True
            
        # Return JSON response for frontend JavaScript
        return JsonResponse({"liked":liked,
                             "status": "success",
                             "like_count": post.likes.count()})    
        
        
@login_required       
def delete_post(request, post_id):
    """Handles the deletion of a post.
    Only the post owner should be able to delete their post.
    This view is designed for AJAX (DELETE) requests. """
    
    # Check if method is DELETE
    if request.method == "DELETE":
        user=request.user       
        post = Post.objects.get(id=post_id)
        
        # Delete the post
        post.delete()
        
        # Return JSON response to confirm deletion
        return JsonResponse({
                             "success": True,
                             })  
    
    

    
    
    
def edit_post(request, post_id):
    """Handles editing of a post's content.
    Only the post owner can edit their post.
    Designed for AJAX POST requests with JSON payload."""
    
    # Check if method is POST
    if request.method == "POST":
        data = json.loads(request.body) 
        newContent = data.get("content", "")
        
        # Get the post
        post = Post.objects.get(id=post_id)
        
        # Update the post content
        post.content=newContent
        post.save()


        # Return JSON response with the updated content
        return JsonResponse({"status": "success", "content": newContent})    
    
    

  

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
