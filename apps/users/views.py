from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.views import View
from users.forms import RegisterForm
from users.models import User, Profile



class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request):
        form = RegisterForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verify_url = request.build_absolute_uri(
                f'/accounts/verify-email/{uid}/{token}/'
            )
            send_mail(
                subject='Email verification - Igrovorot',
                message=f'Click to verify your email: {verify_url}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
            )
            messages.success(request, 'На почту отправлено письмо для подтверждения.')
            return redirect('login')
        return render(request, self.template_name, {'form': form})


class VerifyEmailView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError):
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'Email подтверждён, добро пожаловать!')
            return redirect('home')
        else:
            messages.error(request, 'Ссылка недействительна или устарела.')
            return redirect('login')

class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        form = AuthenticationForm(request)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        messages.error(request, 'Неверный email или пароль.')
        return render(request, self.template_name, {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class ProfileView(View):
    template_name = 'users/profile.html'

    def get(self, request, username):
        profile_user = get_object_or_404(User, username=username)
        profile, _ = Profile.objects.get_or_create(user=profile_user)
        return render(request, self.template_name, {
            'profile_user': profile_user,
            'profile': profile,
        })