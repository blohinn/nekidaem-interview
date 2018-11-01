from django.urls import path
from . import views

app_name = 'blog_app'
urlpatterns = [
    path('add-article/', views.CreateArticle.as_view(), name='add_article'),
    path('edit-article/<int:pk>/', views.EditArticle.as_view(), name='edit_article'),
    path('delete-article/<int:pk>', views.DeleteArticle.as_view(), name='delete_article'),

    path('<int:pk>/', views.BlogArticleList.as_view(), name='blog_articles'),
    path('article/<int:pk>', views.BlogArticleDetail.as_view(), name='article_detail')
]
