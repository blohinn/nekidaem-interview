from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView

from .models import BlogArticle, Blog
from .forms import BlogArticleForm


class CreateEditArticle(LoginRequiredMixin, View):
    form_class = BlogArticleForm
    template_name = 'blog_app/create_edit_article.html'

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            blog_article = get_object_or_404(BlogArticle, pk=kwargs['pk'])
            form = self.form_class(instance=blog_article)
        else:
            form = self.form_class()

        return render(request, self.template_name, {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            blog_article = form.save(commit=False)
            blog_article.blog = request.user.blog
            blog_article.save()
            return redirect('/')

        return render(request, self.template_name, {
            'form': form
        })


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
