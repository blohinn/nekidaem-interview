from django.urls import path
from . import views

app_name = 'feed_app'
urlpatterns = [
    path('subscriptions/', views.SubscriptionList.as_view(), name='subscriptions'),
    path('subscriptions/subscribe/<int:pk>/', views.Subscribe.as_view(), name='subscribe'),
    path('subscriptions/unsubscribe/<int:pk>/', views.Unsubscribe.as_view(), name='unsubscribe'),
    path('', views.Feed.as_view(), name='feed')
]
