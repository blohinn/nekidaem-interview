from django.urls import path
from . import views

app_name = 'blog_app'
urlpatterns = [
    path('add-article/', views.CreateEditArticle.as_view()),
    path('edit-article/<int:pk>/', views.CreateEditArticle.as_view()),
    path('<str:username>/', views.BlogArticleList.as_view())
]
