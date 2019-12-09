from django.db.models.signals import post_save
from .models import Post
from django.dispatch import receiver


@receiver(post_save, sender=Post)
def check_publish_permission(sender, instance, created, **kwargs):
    if created:
        if instance.author.has_perm('blog.publish_without_moderation'):
            instance.status = Post.Status.PUBLISHED
            instance.save()
