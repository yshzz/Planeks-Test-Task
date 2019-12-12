from django.shortcuts import render
from django.views import View
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.views.generic import ListView, CreateView, DetailView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin
from .models import Post
from .forms import CommentForm


class PostListView(ListView):
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    fields = ('title', 'content')
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDisplay(DetailView):
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object = self.get_object()

        context['c_form'] = CommentForm
        return context


class Comment(SingleObjectMixin, FormView):
    template_name = 'blog/post_detail.html'
    form_class = CommentForm
    model = Post

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('blog:post-detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = self.object
        form.save()
        return super().form_valid(form)


class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        view = PostDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = Comment.as_view()
        return view(request, *args, **kwargs)


def about(request):
    return render(request, 'blog/about.html')
