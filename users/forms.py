from django import forms
from cuser.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Profile
from datetime import date
from .validators import validate_email

current_year = date.today().year
BIRTH_YEAR_CHOICES = [
    year for year in range(current_year - 100, current_year + 1)
]


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label=_('Email Address'),
        max_length=254,
        # validators=[validate_email],
        widget=forms.EmailInput(attrs={'autofocus': True})
    )
    first_name = forms.CharField(
        label=_('First Name'),
        max_length=30,
        required=False
    )
    last_name = forms.CharField(
        label=_('Last Name'),
        max_length=150,
        required=False
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2', 'first_name', 'last_name')


class ProfileRegisterForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES),
        label=_('Birth Date'),
        required=False
    )

    class Meta:
        model = Profile
        fields = ('birth_date',)
