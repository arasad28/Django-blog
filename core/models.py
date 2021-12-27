from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.urls import reverse
from ckeditor.fields import RichTextField
# Create your models here.
User=get_user_model()



category_choice=(
    ('Travel','Travel'),
    ('Lifestyle','Lifestyle'),
    ('Photography','Photography'),
    ('Culinary','Culinary'),
    ('Fashion','Fashion'),
    ('Work','Work'),
    ('Business','Business')
)



class Comments(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    content=models.TextField()
    post=models.ForeignKey('Post',related_name='comments',on_delete=models.CASCADE)


    def __str__(self):
        return self.user.username

class Author(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    profile_picture=models.ImageField()

    def __str__(self):
        return self.user.username

class Post(models.Model):
    title=models.CharField(max_length=100)
    thumbnail_img=models.ImageField()
    overview=models.TextField()
    content=RichTextField(blank=True,null=True)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    comment_count=models.IntegerField(default=0)
    featured=models.BooleanField()
    slider=models.BooleanField(default=False)
    category=models.CharField(choices=category_choice,max_length=20)
    read=models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('page', kwargs={
            'id':self.id
        })
    def post_update_url(self):
        return reverse('post-update',kwargs={
            'id':self.id
        })
    def post_delete_url(self):
        return reverse('post-delete',kwargs={
            'id':self.id
        })
    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')
