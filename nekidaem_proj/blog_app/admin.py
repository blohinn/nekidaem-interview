from django.contrib import admin
from django import forms
from django.core.exceptions import ValidationError

from .models import Blog, BlogArticle


class BlogAdminForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = '__all__'

    def clean(self):
        if self.cleaned_data.get('owner') in self.cleaned_data.get('subscribers'):
            raise ValidationError("You can't be subscribed to yourself.")
        return super(BlogAdminForm, self).clean()


class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ('name', 'owner')


class BlogArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'blog', 'owner', 'created')
    raw_id_fields = ('blog',)

    def owner(self, obj):
        return obj.blog.owner.username


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogArticle, BlogArticleAdmin)
