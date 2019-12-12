import logging
from django.urls import reverse
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from news_site.celery import app
from blog.models import Comment
from .mailgun import Mailgun

mg = Mailgun()


@app.task
def send_verification_email(user_id, scheme, domain):
    User = get_user_model()

    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        logging.warning(
            f'Tried to send verification email to non-existing user {user_id}'
        )

    kwargs = {
        'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user)
        }
    url = reverse('activate', kwargs=kwargs)
    activation_link = f'{scheme}://{domain}{url}'
    to = user.email
    subject = 'Activate account'
    text = f'Activate account: {activation_link}'
    mg.send_email(to=to, subject=subject, text=text)


@app.task
def send_notification_email(author_id, comment_id):
    User = get_user_model()

    try:
        user = User.objects.get(pk=author_id)
        comment = Comment.objects.get(pk=comment_id)
    except User.DoesNotExist:
        logging.warning(
            f'Tried to send notification to non-existing user {author_id}'
        )
    except Comment.DoesNotExist:
        logging.warning(
            f'Tried to send notification about non-existing comment {comment_id}'
        )

    to = user.email
    subject = 'New comment'
    text = f'{comment.author.email} has commented your post "{comment.post.title}"'
    mg.send_email(to=to, subject=subject, text=text)
