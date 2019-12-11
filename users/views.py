from django.shortcuts import render, redirect
from .forms import UserRegisterForm, ProfileRegisterForm


def register(request):
    if request.method == 'POST':
        u_form = UserRegisterForm(request.POST)
        p_form = ProfileRegisterForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            user.refresh_from_db()

            p_form = ProfileRegisterForm(
                request.POST,
                instance=user.profile
            )
            p_form.full_clean()
            p_form.save()

            return redirect('blog:home')
    else:
        u_form = UserRegisterForm()
        p_form = ProfileRegisterForm()
    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/register.html', context)
