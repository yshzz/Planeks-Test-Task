from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from .forms import UserRegisterForm, ProfileRegisterForm
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_text
from .tokens import account_activation_token
from .tasks import send_verification_email

User = get_user_model()


def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        p_form = ProfileRegisterForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save(commit=False)
            user.is_active = False
            user.save()
            user.refresh_from_db()

            p_form = ProfileRegisterForm(
                request.POST,
                instance=user.profile
            )
            p_form.full_clean()
            p_form.save()

            scheme = request.scheme
            domain = get_current_site(request).domain
            send_verification_email.delay(user.id, scheme, domain)
            return redirect('activate-done')
    else:
        u_form = UserRegisterForm()
        p_form = ProfileRegisterForm()
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/register.html', context)


def activate_done(request):
    return render(request, 'users/activate_done.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request,
            'Your account has been created! You are now able to log in!'
        )
        return redirect('login')
    else:
        return HttpResponse('Invalid Token')
