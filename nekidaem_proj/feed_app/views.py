from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView

from blog_app.models import Blog


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
        return redirect(reverse('feed_app:subscriptions'))
