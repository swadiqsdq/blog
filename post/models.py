from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    created_user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)

    def __str__(self):
        return self.title
    
# comment section 
class Comments(models.Model):
    comment_text = models.CharField(max_length=250)
    comment_auther = models.ForeignKey(User,on_delete=models.CASCADE)
    blog_data = models.ForeignKey(Post,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now_add=True)
    