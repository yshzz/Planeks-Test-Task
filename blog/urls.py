from django.urls import path
from .views import PostListView, PostCreateView, PostDetailView, about

app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('about/', about, name='about'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
]
