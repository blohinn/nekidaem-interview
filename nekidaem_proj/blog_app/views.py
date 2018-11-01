from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import BlogArticle, Blog
from .forms import BlogArticleForm


class CreateArticle(LoginRequiredMixin, CreateView):
    form_class = BlogArticleForm
    template_name = 'blog_app/create_edit_article.html'

    def form_valid(self, form):
        blog_article = form.save(commit=False)
        blog_article.blog = self.request.user.blog
        blog_article.save()
        return redirect(self.get_success_url())

    def get_success_url(self):
        return reverse('blog_app:blog_articles', args=[self.request.user.blog.pk])


class EditArticle(LoginRequiredMixin, UpdateView):
    form_class = BlogArticleForm
    template_name = 'blog_app/create_edit_article.html'

    def get_object(self, queryset=None):
        article = get_object_or_404(BlogArticle, pk=self.kwargs['pk'])
        if article.blog.owner != self.request.user:
            raise PermissionDenied()
        return article

    def get_success_url(self):
        return reverse('blog_app:article_detail', args=[self.kwargs['pk']])


class DeleteArticle(LoginRequiredMixin, DeleteView):
    def get_object(self, queryset=None):
        article = get_object_or_404(BlogArticle, pk=self.kwargs['pk'])
        if article.blog.owner != self.request.user:
            raise PermissionDenied()
        return article

    def get_success_url(self):
        return reverse('blog_app:blog_articles', args=[self.request.user.blog.pk])


class BlogArticleList(ListView):
    template_name = 'blog_app/list_articles.html'
    paginate_by = 10

    blog = None

    def get_queryset(self):
        self.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return self.blog.articles.order_by('-created').all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = self.blog
        return context


class BlogArticleDetail(DetailView):
    template_name = 'blog_app/detail_article.html'
    model = BlogArticle
    context_object_name = 'article'


class BlogList(ListView):
    template_name = 'blog_app/list_blog.html'
    queryset = Blog.objects.order_by('owner__username').all()
