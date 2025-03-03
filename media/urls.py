from django.urls import path
from . import views 
 # Import views from the same app
from django.contrib.auth import views as auth_views

urlpatterns = [
     # Root URL for the app
    path('signup/', views.signup_view, name='signup'),  # ✅ Use signup_vi
    path('', views.login_view, name='login'),
    path('feed/', views.feed_view, name='feed'),  # ✅ Use login_view
    path('logout/', views.logout_view, name='logout'),
    path('post/create/', views.post_createview, name='post_create'),
    path('profile/', views.profile_view, name='profile'),
    path('home/', views.home, name='home'),
    path('friendrequests/', views.friend_requests, name='friend_requests'),
    path('like/<int:post_id>/', views.like_post, name='like'),
    path("friend_requests/", views.friend_request_view, name="friend_requests"),
    path("send_friend_request/<int:user_id>/", views.send_friend_request, name="send_friend_request"),
    path("accept_friend_request/<int:request_id>/", views.accept_friend_request, name="accept_friend_request"),
    path("reject_friend_request/<int:request_id>/", views.reject_friend_request, name="reject_friend_request"),
    path("delete_post/<int:post_id>/", views.delete_post, name="delete_post"),

]