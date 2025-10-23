
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("following/", views.following, name="following"),
    path("follow/<str:username>/", views.followUser, name="follow_user"),
    path("profile/<str:username>/showFollowers/", views.showFollowers, name="showFollowers"),
    path("profile/<str:username>/showFollowing/", views.showFollowing, name="showFollowing"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("edit/<int:post_id>/",views.edit_post, name="edit_post"),
    path("like/<int:post_id>/",views.like_post, name="like_post"),
    path("delete/<int:post_id>/",views.delete_post, name="delete_post")


   


]
