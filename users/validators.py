from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .mailgun import Mailgun

EXPECTED_RESULT = 'deliverable'
mg = Mailgun()


def validate_email(email):
    verification = mg.validate_email(email)
    if verification['result'] != EXPECTED_RESULT:
        raise ValidationError(_(
            'You have entered undeliverable email address, '
            'please enter real email address.'
        ))
