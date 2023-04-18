from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect

User = get_user_model()


def register_page(request):
    data = {
        "fname" : "",
        "lname" : "",
        "email": "",
        "password": "",
        "cpassword": ""
    }
    return render(request, "auth/register.html", data)


def register_user(request):
    try:
        fname = request.GET.get('fname').capitalize()
        lname = request.GET.get('lname').capitalize()
        email = request.GET.get('email')
        password = request.GET.get('regPwd')
        cpassword = request.GET.get('confirmRegPwd')
        print(request.GET)
        data = {
            "fname" : fname,
            "lname" : lname,
            "email": email,
            "password": password,
            "cpassword": cpassword
        }

        # Check if fields empty
        if not fname or not lname or not email or not password or not cpassword:
            data['error'] = True
            data['error_msg'] = "All fields are requiredy"
            return render(request, "auth/register.html", data)

        # Check for email
        if '@' not in email:
            data['error'] = True
            data['error_msg'] = "Invalid email address"
            return render(request, "auth/register.html", data)

        # Check for password and confirm password
        if password != cpassword:
            data['error'] = True
            data['error_msg'] = "Passwords do not match"
            return render(request, "auth/register.html", data)


        # Check if user already exists with the same email
        qs = User.objects.filter(email=email)
        if qs.exists():
            data['error'] = True
            data['error_msg'] = "Passwords do not match"
            return render(request, "auth/register.html", data)

        new_user = User.objects.create_user(email, password=password, first_name=fname, last_name=lname, )
        new_user.email = email
        new_user.username = "to123"
        new_user.is_active = True
        new_user.is_staff = False
        new_user.save()

        login(request, new_user)

        return redirect("/app")
    except Exception as e:
        data = {
            "fname" : "",
            "lname" : "",
            "email": "",
            "password": "",
            "cpassword": ""
        }
        data['error'] = True
        data['error_msg'] = "something went wrong {}".format(str(e))
        return render(request, "auth/register.html", data)

