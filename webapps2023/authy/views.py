from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

User = get_user_model()


def login_page(request):
    data = {
        "email": "",
        "password": ""
    }
    return render(request, "auth/login.html", data)


def login_user(request):
    try:
        email = request.POST.get('email', "")
        password = request.POST.get('password', "")

        data = {
            "email": email,
            "password": password
        }

        print(data)
        user = authenticate(username=email, password=password)
        print(user)

        if user is not None and user.is_active:
            login(request, user)

            if request.user.is_staff and request.user.is_superuser:
                return redirect('/admin')
            elif request.user.is_staff:
                return redirect('/admin')
            else:
                return redirect('/app')
        else:
            data['error'] = True
            data['error_msg'] = "Invalid Username and Password"

        return render(request, "auth/login.html", data)
    except Exception as e:
        data = {
            "email": "",
            "password": ""
        }
        data['error'] = True
        data['error_msg'] = "Something went wrong {}".format(str(e))
        return render(request, "auth/login.html", data)

@login_required
def change_password(request):
    data = {}

    if request.method == 'POST':
        old_password = request.POST['oldPwdInput']
        new_password = request.POST['newPwdInput']
        user = request.user

        if not user.check_password(old_password):
            data['error'] = True
            data['error_msg'] = "The old password you entered is incorrect."
            messages.error(request, 'The old password you entered is incorrect.')
            return redirect('change_password')

        if len(new_password) < 8:
            data['error'] = True
            data['error_msg'] = "The new password must be at least 8 characters long."
            messages.error(request, 'The new password must be at least 8 characters long.')
            return redirect('change_password')

        user.set_password(new_password)
        user.save()

        messages.success(request, 'Your password has been updated.')
        return redirect('home')

    return render(request, "app/settings.html")


def logout_user(request):
    data = {}
    logout(request)

    return render(request, "auth/login.html", data)
