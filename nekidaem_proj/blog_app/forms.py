from django import forms
from .models import BlogArticle


class BlogArticleForm(forms.ModelForm):
    class Meta:
        model = BlogArticle
        fields = ('title', 'body')
