from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    """Model representing a user's post in the social network.
    Each post has an author (user), text content, timestamp, and likes. """
    
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content= models.CharField(max_length=500)
    timestamp= models.DateTimeField(auto_now_add=True)
    likes=models.ManyToManyField(User,blank=True,related_name="likes")
    
    
    def __str__(self):
        
        """Readable representation of a post, showing short content and date."""
        
        format = "%B %d, %Y %I:%M%p"

        return f" {self.content} {self.timestamp.strftime(format)}"
    
    
    
     
    
class Follow(models.Model):
    """Represents a 'follow' relationship between two users. 'follower' follows 'following'."""
    
    follower=models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following=models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    followStatus=models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('follower', 'following')
        
    def __str__(self):
        return f"{self.follower.username} → {self.following.username}"

    
    
    