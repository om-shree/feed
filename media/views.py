from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User  # Use Django's built-in User model
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Post
from .forms import PostForm
from .models import FriendRequest


# ✅ Signup View - Use Django's User Model
def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username and email and password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
                return redirect('signup')

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered!")
                return redirect('signup')

            # 🔹 Create User with Django's Authentication System
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Signup successful! You can now log in.")
            return redirect('login')  # Redirect to login page

    return render(request, 'signup.html')

# ✅ Login View - Authenticate User Properly
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")  # Use username instead of email
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)  # Authenticate using username
        
        if user is not None:
            login(request, user)  # 🔹 Log the user in
            messages.success(request, "Login successful!")
            return redirect('feed')  # Redirect to feed after login
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

# ✅ Feed View - Show Posts
@login_required(login_url='/login/')  # Ensure user is logged in
def feed_view(request):
    posts = Post.objects.all().order_by("-created_at")
    return render(request, "feed.html", {"posts": posts})

# ✅ Logout View - Proper Logout Handling
def logout_view(request):
    logout(request)  # 🔹 Django's logout function
    messages.success(request, "Logged out successfully.")
    return redirect('login')

# ✅ Post Creation View - Now Uses Authenticated User
@login_required(login_url='/login/')  # 🔹 Ensure only logged-in users can access
def post_createview(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # ✅ request.user is now properly authenticated
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('feed')
        else:
            print("Form Errors:", form.errors)  # Debugging

    else:
        form = PostForm()

    return render(request, 'post_create.html', {'form': form})

# ✅ Profile View - Show User's Posts
@login_required(login_url='/login/')  
def profile_view(request):
    user = request.user
    posts = Post.objects.filter(user=user)  # Get posts of the logged-in user
    return render(request, 'profile.html', {'user': user, 'posts': posts})

# ✅ Home View
def home(request):
    return render(request, 'home.html')

# ✅ Friend Requests View
@login_required(login_url='/login/')  
def friend_requests(request):
    return render(request, 'friend_requests.html')


from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Post

def like_post(request, post_id):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, id=post_id)
        
        # Toggle Like: Add if not liked, remove if already liked
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        
        return JsonResponse({"success": True, "liked": liked, "likes_count": post.likes.count()})
    
    return JsonResponse({"success": False, "error": "User not authenticated"}, status=403)


def delete_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, id=post_id, user=request.user)
        post.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


def friend_request_view(request):
    users = User.objects.exclude(id=request.user.id)
    friend_requests = FriendRequest.objects.filter(receiver=request.user, status="pending")
    
    return render(request, "friendrequest.html", {"users": users, "friend_requests": friend_requests})

def send_friend_request(request, user_id):
    if request.method == "POST":
        receiver = get_object_or_404(User, id=user_id)
        friend_request, created = FriendRequest.objects.get_or_create(sender=request.user, receiver=receiver)
        
        if created:
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False, "message": "Request already sent"})

def accept_friend_request(request, request_id):
    if request.method == "POST":
        friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
        friend_request.status = "accepted"
        friend_request.save()
        return JsonResponse({"success": True})

def reject_friend_request(request, request_id):
    if request.method == "POST":
        friend_request = get_object_or_404(FriendRequest, id=request_id, receiver=request.user)
        friend_request.status = "rejected"
        friend_request.delete()
        return JsonResponse({"success": True})

