from django.contrib import admin

from .models import Blog, BlogArticle


class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner')


class BlogArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'blog', 'owner', 'created')
    raw_id_fields = ('blog',)

    def owner(self, obj):
        return obj.blog.owner.username


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogArticle, BlogArticleAdmin)
