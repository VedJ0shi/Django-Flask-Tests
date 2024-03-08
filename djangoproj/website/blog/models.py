from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Blogpost(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "posts") #User is the related table (model class)
    #author will be an object of the User model class

    def __str__(self):
        return f"{self.title}|{len(self.content)} chars|by {self.author}"