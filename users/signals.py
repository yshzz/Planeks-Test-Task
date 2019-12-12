from enum import Enum
from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Profile
from .exceptions import DefaultGroupNotFound
from blog.models import Comment
from .tasks import send_notification_email

User = get_user_model()


class DefaultGroup(Enum):
    USERS = 'users'
    REDACTORS = 'redactors'
    ADMINS = 'admins'


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def add_to_users_group(sender, instance, created, **kwargs):
    if not instance.is_superuser and created:
        try:
            users_group = Group.objects.get(name=DefaultGroup.USERS.value)
        except Group.DoesNotExist:
            raise DefaultGroupNotFound(DefaultGroup.USERS.value)
        instance.groups.add(users_group)


"""
Make every user added to 'admins' group a staff member and make every user
removed from 'admins' group not a staff member.
"""
@receiver(signal=m2m_changed, sender=User.groups.through)
def manage_admins(instance, action, reverse, model, pk_set, *args, **kwargs):
    actions = ('post_add', 'post_remove')

    if (model == Group) and (action in actions):
        try:
            admins_group_pk = Group.objects.get(
                name=DefaultGroup.ADMINS.value
            ).pk
        except Group.DoesNotExist:
            raise DefaultGroupNotFound(DefaultGroup.ADMINS.value)
        if admins_group_pk in pk_set:
            if action == actions[0]:
                instance.is_staff = True
            else:
                instance.is_staff = False
            instance.save()


@receiver(post_save, sender=Comment)
def notify_post_author(sender, instance, created, **kwargs):
    if created:
        author_id = instance.post.author.id
        comment_id = instance.id
        send_notification_email.delay(author_id, comment_id)
