from django.contrib import messages
from django.contrib.auth import login, authenticate, logout,\
    update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View

from apps.user.messages.messages import send_activation_link

from .forms import SignUpForm, LogInForm, ChangePasswordForm
from .models import User
from .tokens import account_activation_token


class Index(View):

    def get(self, request):
        return render(request, 'mainpage.html')


class SignUp(View):

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            receiver = form.cleaned_data.get('email')
            send_activation_link(request, user, receiver)
            return render(request, 'registration/after_signup.html')

        context = {
            'form': form
        }
        return render(request, 'registration/signup.html', context)

    def get(self, request):
        form = SignUpForm()
        return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class LogIn(View):

    def post(self, request):
        form = LogInForm(request.POST)

        if form.is_valid():
            user = form.login(request)
            if user:
                login(request, user)
            if request.GET.get('next'):
                return redirect(request.GET['next'])
            return redirect('index')
        context = {
            'form': form,
        }

        return render(request, 'registration/signup.html', context)

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profile')
        else:
            form = LogInForm()
            return render(request, 'registration/login.html', {'form': form})


class LogOut(View):

    def get(self, request):
        logout(request)
        return render(request, 'registration/logout.html')


class ChangePassword(View):

    def post(self, request):
        form = ChangePasswordForm(request.user, request.POST)

        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')

    def get(self, request):

        form = ChangePasswordForm(request.user)
        return render(request, 'registration/change_password.html',
                      {'form': form})

# DODAJ ZAPISYWANIE FORMA i wyciągaj z request.user jako instancja do one to one do USER ! ! !  # Noqa
#@method_decorator(login_required, name='dispatch')
#class Profile(View):

  #  def get(self, request):
  #      form = UserDetailsForm()
  #      user_data = User.objects.get(pk=request.user.pk)

  #      context = {
  #          'user_data': user_data,
  #          'form': form,cd .
 #           'user_details': user_details
 #       }
 #       return render(request, 'profile.html', context)
##
  #  def post(self, request):
  #      form = UserDetailsForm(request.POST)
 #       user_data = User.objects.get(pk=request.user.pk)
 #       print(user_data)
 #       context = {
 #           'user_data': user_data,
#            'form': form,
#        }
  #      return render(request, 'profile.html', context)



#that's some minor change to check ssh some more changes