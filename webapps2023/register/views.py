from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from currency.models import Currency
from authy.models import UserWallet
import requests

User = get_user_model()


def register_page(request):
    data = {
        "fname": "",
        "lname": "",
        "email": "",
        "password": "",
        "cpassword": "",
        "currency": ""
    }
    return render(request, "auth/register.html", data)


def register_user(request):
    try:
        fname = request.GET.get('fname').capitalize()
        lname = request.GET.get('lname').capitalize()
        email = request.GET.get('email').lower()
        password = request.GET.get('regPwd')
        cpassword = request.GET.get('confirmRegPwd')
        currency = request.GET.get('accCurrency')

        data = {
            "fname": fname,
            "lname": lname,
            "email": email,
            "password": password,
            "cpassword": cpassword,
            "currency": currency
        }

        # Check if fields empty
        if not fname or not lname or not email or not password or not cpassword or not currency:
            data['error'] = True
            data['alert'] = True
            data['error_msg'] = "All fields are required"

            return render(request, "auth/register.html", data)

        # Check for email
        if '@' not in email:
            data['error'] = True
            data['alert'] = True
            data['error_msg'] = "Invalid email address"

            return render(request, "auth/register.html", data)

        # Check for password and confirm password
        if password != cpassword:
            data['error'] = True
            data['alert'] = True
            data['error_msg'] = "Passwords do not match"

            return render(request, "auth/register.html", data)

        # Check if user already exists with the same email
        qs = User.objects.filter(email=email)
        if qs.exists():
            data['error'] = True
            data['alert'] = True
            data['error_msg'] = "Email already exist"

            return render(request, "auth/register.html", data)

        # Check if support currency
        cs = Currency.objects.filter(code=currency)
        if not cs.exists():
            data['error'] = True
            data['alert'] = True
            data['error_msg'] = "We don't support this currency type"

            return render(request, "auth/register.html", data)

        new_user = User.objects.create_user(email, password=password, first_name=fname, last_name=lname, )
        new_user.email = email
        username_array = email.split("@")
        username = "#{}".format(username_array[0])
        new_user.username = username
        new_user.is_active = True
        new_user.is_staff = False

        currency = Currency.objects.get(code=currency)

        if currency.code == "gbp":
            wallet = UserWallet.create(new_user, currency, balance=1000.00)
        else:
            response = requests.get("http://{}/conversion/gbp/{}/1000".format(request.get_host(), currency.code))
            response_data = response.json()
            data = response_data.get("data", dict())
            converted_amount = data.get("amount", 0)
            wallet = UserWallet.create(new_user, currency, balance=converted_amount)

        wallet.is_active = True
        wallet.save()
        new_user.save()

        login(request, new_user)

        data['error'] = True
        data['alert'] = False
        data['error_msg'] = "Account registration successful"

        return redirect("/app")
        # return render(request, "payapp/dashboard.html", data)
    except Exception as e:
        data = {
            "fname": "",
            "lname": "",
            "email": "",
            "password": "",
            "cpassword": "",
            "currency": ""
        }
        data['error'] = True
        data['alert'] = True
        data['error_msg'] = "Something went wrong {}".format(str(e))
        return render(request, "auth/register.html", data)
