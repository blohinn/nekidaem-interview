from django.urls import path
from . import views

app_name = 'blog_app'
urlpatterns = [
    path('add-article/', views.CreateEditArticle.as_view()),
    path('edit-article/<int:pk>/', views.CreateEditArticle.as_view()),
    path('<int:pk>/', views.BlogArticleList.as_view(), name='blog_articles'),
    path('article/<int:pk>', views.BlogArticleDetail.as_view(), name='article_detail')
]
