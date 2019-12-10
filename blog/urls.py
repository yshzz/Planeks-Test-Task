from django.urls import path
from .views import PostListView, about

app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('about/', about, name='about'),
]
