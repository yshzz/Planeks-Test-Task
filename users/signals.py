from django.db.models.signals import post_save, m2m_changed
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Profile
from .exceptions import DefaultGroupNotFound

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=User)
def add_to_users_group(sender, instance, created, **kwargs):
    if created:
        try:
            users_group = Group.objects.get(name='users')
        except Group.DoesNotExist:
            raise DefaultGroupNotFound('users')
        instance.groups.add(users_group)


"""Make every user added to 'admins' group a staff member."""
@receiver(signal=m2m_changed, sender=User.groups.through)
def manage_admins(instance, action, reverse, model, pk_set, *args, **kwargs):
    if model == Group and action == 'post_add':
        try:
            admins_group_pk = Group.objects.get(name='admins').pk
        except Group.DoesNotExist:
            raise DefaultGroupNotFound('admins')
        if admins_group_pk in pk_set:
            instance.is_staff = True
            instance.save()
