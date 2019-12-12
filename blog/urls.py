from django.urls import path
from .views import PostListView, PostCreateView, about

app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('about/', about, name='about'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
]
