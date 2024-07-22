from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="post")
    content = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "username": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

class Like(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="like")
    post = models.ForeignKey("Post",on_delete=models.CASCADE, related_name="likedPost")

    def serial(self):
        return {
            "id": self.id,
            "username": self.user.username,
            "post": self.post
        }
    
    
class Followers(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="follower")
    followers = models.ForeignKey("User",on_delete=models.CASCADE, related_name="userFollowed")

    def serl(self):
        return {
            "id": self.id,
            "username": self.user.username,
            "post": self.followers
        }