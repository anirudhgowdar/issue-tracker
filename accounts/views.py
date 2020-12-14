from django.http import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth import authenticate, update_session_auth_hash
from . import forms
from django.contrib.auth.models import User


def register(request):
    form = None
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')
            return redirect('accounts:login')
    elif request.method == 'GET':
        form = forms.RegisterForm()
    return render(
        request=request,
        template_name='accounts/register.html',
        context={'form': form}
    )


def login(request):
    if request.method == 'POST':
        form = forms.LoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(
                    request, f"You are now logged in as {username}")
                return redirect('accounts:dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = forms.LoginForm()
    return render(
        request=request,
        template_name='accounts/login.html',
        context={"form": form}
    )


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('home:index')


def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/dashboard.html')
    else:
        return render(request, 'accounts/error.html')


def profile(request, user_id):
    userdata = User.objects.get(pk=user_id)
    return render(request, 'accounts/profile.html', {'userdata': userdata})


def edit_profile(request, user_id):
    if user_id:
        user = get_object_or_404(User, pk=user_id)

    form = forms.EditProfileForm(request.POST or None, instance=user)
    if request.POST and form.is_valid():
        form.save()
        messages.success(request, 'Profile Updated Successfully')
        # Save was successful, so redirect to another page
        return redirect('accounts:dashboard')

    return render(request, 'accounts/edit_profile.html', {
        'form': form
    })


def change_password(request):
    if request.method == 'POST':
        form = forms.ChangePasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(
                request, 'Your password was successfully updated!')
            auth.logout(request)
            return redirect('accounts:login')
    else:
        form = forms.ChangePasswordForm(request.user)
    return render(request, 'accounts/change_password.html', {
        'form': form
    })
