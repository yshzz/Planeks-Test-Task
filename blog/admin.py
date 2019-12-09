from django.contrib import admin
from .models import Post, Comment


def approve(modeladmin, request, queryset):
    queryset.update(status=Post.Status.PUBLISHED)
    approve.short_description = "Approve post"


def decline(modeladmin, request, queryset):
    queryset.update(status=Post.Status.UNPUBLISHED)
    approve.short_description = "Decline post"


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    actions = [approve, decline]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
