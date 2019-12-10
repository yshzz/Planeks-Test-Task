from django.shortcuts import render
from django.views.generic import ListView
from .models import Post


class PostListView(ListView):
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


def about(request):
    return render(request, 'blog/about.html')
