from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime

# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class DraftManager(models.Manager):
    def get_queryset(self):
        return super(DraftManager,self).get_queryset().filter(status='draft')




class Post(models.Model):
    STATUS_CHOICES=(
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique_for_date='publish')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()
    published = PublishedManager()
    draft = DraftManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering=('-publish', 'title',)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, 
                                    self.publish.strftime('%m'),
                                    self.publish.strftime('%d'),
                                    self.slug])
    
    def share_url(self):
        return reverse('blog:post_share', args=[self.id])

class Comment(models.Model):
    post=models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name=models.CharField(max_length=50)
    email=models.EmailField()
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)

    class Meta:
        ordering=('created',)
    