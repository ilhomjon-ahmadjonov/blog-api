from django.db import models
from user.models import Customuser
# Create your models here.


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Post(TimeStampedModel):
    author = models.ForeignKey(Customuser,on_delete=models.CASCADE,related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    def __str__(self):
        return self.title

class Comment(TimeStampedModel):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(Customuser,on_delete=models.CASCADE,related_name='comments')
    text = models.TextField()

    def __str__(self):
        return f'{self.author}-{self.post.title}'

class Like(TimeStampedModel):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='likes')
    user = models.ForeignKey(Customuser,on_delete=models.CASCADE,related_name='likes')

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'{self.user} likes {self.post}'

class PostView(TimeStampedModel):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='views')
    user = models.ForeignKey(Customuser,on_delete=models.CASCADE,related_name='post_views')

    class Meta:
        unique_together = ('post','user')

        def __str__(self):
            return f'{self.user} viewed {self.post}'
        