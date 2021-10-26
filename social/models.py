from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator

# Create your models here.
class MyProfile(models.Model):
    name = models.CharField(max_length=100)
    phoneno = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    #name = models.OneToOneField(to=User, on_delete=CASCADE)
    user = models.OneToOneField(to=User, on_delete=CASCADE)
    status = models.CharField(max_length=20, default= "single" ,choices=(("single","single"), ("married","married")))
    gender = models.CharField(max_length=20, default= "male" ,choices=(("male","male"), ("female","female")))
    age =models.IntegerField(default=18, validators=[MinValueValidator(18),MaxValueValidator(100)])
    #phoneno = models.CharField(validators=[RegexValidator("^0?[5-9]{1}\d{9}$")], max_length=15, null=True,blank=True)
    address = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to = "image\\", null=True)
    def __str__(self):
        #return self.user.username
        #return "%s (%s)" %(self.user.username)
        return "%s" % self.user


class MyPost(models.Model):
    pic = models.ImageField(upload_to = "image\\", null=True)
    subject = models.CharField(max_length=200)
    msg = models.TextField(null=True, blank=True)
    cr_date = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE, null=True)
    
    
    def __str__(self):
        return "%s" % self.subject


class PostComment(models.Model):
    post = models.ForeignKey(to=MyPost, on_delete=CASCADE)
    msg = models.TextField(null=True, blank=True)
    commented_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)
    flag = models.CharField(max_length=20, null=True, blank=True ,choices=(("racist","racist"), ("abusing","abusing")))
    
    def __str__(self):
        return "%s" % self.msg

class PostLike(models.Model):
    post = models.ForeignKey(to=MyPost, on_delete=CASCADE)
    liked_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE)
    cr_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return "%s" % self.liked_by

class FollowUser(models.Model):
    profile = models.ForeignKey(to=MyProfile, on_delete=CASCADE, related_name="profile")
    followed_by = models.ForeignKey(to=MyProfile, on_delete=CASCADE, related_name="followed_by")
    def __str__(self):
        return "%s is followed by %s" % (self.profile, self.followed_by)










