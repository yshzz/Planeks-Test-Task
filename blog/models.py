from django.db import models
from django.utils import timezone
from django.conf import settings
from froala_editor.fields import FroalaField
from django.utils.translation import gettext_lazy as _


class Post(models.Model):
    class Status(models.TextChoices):
        PENDING_APPROVAL = 'pending_approval', _('Pending approval')
        PUBLISHED = 'published', _('Published')
        UNPUBLISHED = 'unpublished', _('Unpublished')

    class Meta:
        permissions = [
            ('publish_without_moderation', _('Can publish without moderation')),
        ]

    title = models.CharField(max_length=100)
    content = FroalaField()
    date_posted = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING_APPROVAL
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    text = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'"{self.post.title}" comment'
