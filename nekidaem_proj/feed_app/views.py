from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from blog_app.models import Blog, BlogArticle


class SubscriptionList(LoginRequiredMixin, ListView):
    template_name = 'feed_app/list_subscriptions.html'
    paginate_by = 30

    def get_queryset(self):
        return self.request.user.subscriptions.order_by('owner__username').all()


class Subscribe(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs['pk'])
        if blog.owner != request.user and request.user not in blog.subscribers.all():
            blog.subscribers.add(request.user)
        return redirect(reverse('feed_app:subscriptions'))


class Unsubscribe(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, pk=kwargs['pk'])
        if blog.owner != request.user and request.user in blog.subscribers.all():
            blog.subscribers.remove(request.user)
            self._remove_read_marks_from_unsubscribed_blog(request.user, blog)

        return redirect(reverse('feed_app:subscriptions'))

    def _remove_read_marks_from_unsubscribed_blog(self, user, blog):
        articles = blog.articles.all()
        for a in articles:
            a.read_by.remove(user)


class MarkAsRead(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(BlogArticle, pk=kwargs['pk'])
        if request.user not in article.read_by.all():
            article.read_by.add(request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class MarkAsUnread(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(BlogArticle, pk=kwargs['pk'])
        if request.user in article.read_by.all():
            article.read_by.remove(request.user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class Feed(ListView):
    template_name = 'feed_app/list_feed.html'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return BlogArticle.objects.order_by('-created').all()
        else:
            return BlogArticle.objects.filter(blog__in=self.request.user.subscriptions.all()).order_by('-created').all()
