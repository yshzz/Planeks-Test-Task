# Generated by Django 3.0 on 2019-12-08 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('pending_approval', 'Pending approval'), ('published', 'Published'), ('unpublished', 'Unpublished')], default='pending_approval', max_length=16),
        ),
    ]