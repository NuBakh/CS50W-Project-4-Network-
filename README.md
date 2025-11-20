# 🌐 CS50 Network — Social Network Project

A Django-based social network built for **CS50 Web Programming (Project 4)**.  
Users can make posts, follow others, like/unlike posts, and view feeds with pagination.

[![Watch Demo](https://img.youtube.com/vi/qGCZalS0SrU/0.jpg)](https://youtu.be/qGCZalS0SrU)

---

🏷 Features
✔ User Authentication

Register, login, logout

User profiles display followers/following counts

✔ Posts

Create new text posts

Edit your own posts inline (without full page reload)

Display post author, content, timestamp, and like count

✔ Like/Unlike

Toggle like/unlike for any post

Like count updates dynamically using JavaScript

✔ Follow System

Follow/unfollow other users

“Following” page shows posts from users you follow

✔ Pagination

Posts displayed 10 per page

“Next” and “Previous” buttons navigate older/newer posts

✔ Feed

“All Posts” page shows all posts from all users in reverse chronological order

“Following” page filters to posts from followed users

🗂 URL Overview

/ — All posts feed

/login, /logout, /register — Authentication routes

/following/ — Posts from followed users

/follow/<username>/ — Follow/unfollow user

/profile/<username>/ — User profile page

/profile/<username>/showFollowers/ — Show user's followers

/profile/<username>/showFollowing/ — Show users the person follows

/edit/<post_id>/ — Edit a post

/like/<post_id>/ — Like/unlike a post

/delete/<post_id>/ — Delete a post

💡 Notes

Single‑page dynamic interface handled with JavaScript

Posts, likes, and follows are updated asynchronously without full page reload

Pagination ensures smooth browsing for large post volumes

