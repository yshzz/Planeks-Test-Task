from django.contrib import admin
from .models import Post, Comment


def approve(modeladmin, request, queryset):
    queryset.update(status=Post.Status.PUBLISHED)


def decline(modeladmin, request, queryset):
    queryset.update(status=Post.Status.UNPUBLISHED)


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    actions = [approve, decline]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
