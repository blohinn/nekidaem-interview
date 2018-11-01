from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Blog(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='blog')
    name = models.CharField(max_length=255, default='Personal Blog')

    subscribers = models.ManyToManyField(User, related_name='subscriptions', blank=True)

    def __str__(self):
        return self.name


@receiver(post_save, sender=User)
def create_user_blog(sender, instance, created, **kwargs):
    if created:
        Blog.objects.create(owner=instance)


class BlogArticle(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='articles')

    title = models.CharField(max_length=255)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True, editable=True)

    read_by = models.ManyToManyField(User, related_name='read_articles', blank=True)

    def __str__(self):
        return self.title
