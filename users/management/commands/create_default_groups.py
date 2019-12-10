"""
Create default permission groups (Users, Redactors, Admins)
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
import logging


PERMISSION_GROUPS = [
    ('users', []),
    ('redactors', ['publish_without_moderation']),
    ('admins', [
        'add_post', 'change_post',
        'delete_post', 'view_post',
        'add_comment', 'change_comment',
        'delete_comment', 'view_comment',
        'publish_without_moderation'
    ])
]


class Command(BaseCommand):
    help = 'Creates the necessary groups with the appropriate permissions'

    def handle(self, *args, **options):
        for group, permissions in PERMISSION_GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for codename in permissions:
                try:
                    permission = Permission.objects.get(codename=codename)
                except Permission.DoesNotExist:
                    logging.warning(f"Permission {codename} not found")
                    continue
                new_group.permissions.add(permission)
