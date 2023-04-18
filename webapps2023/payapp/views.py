from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.conf import settings
from currency.models import Currency
from json import dumps

import os

CONVERSION_RATE = [
    {"from": "gbp",
     "to": "gbp",
     "rate": 1.0,
     "img_from": "img/uk.png",
     "img_to": "img/uk.png"
     },
    {"from": "gbp",
     "to": "usd",
     "rate": 1.24,
     "img_from": "img/uk.png",
     "img_to": "img/usa.svg"
     },
    {"from": "gbp",
     "to": "eur",
     "rate": 1.12,
     "img_from": "img/uk.png",
     "img_to": "img/euro.png"
     },
    {"from": "eur",
     "to": "eur",
     "rate": 1.0,
     "img_from": "img/euro.png",
     "img_to": "img/euro.png"
     },
    {"from": "eur",
     "to": "gbp",
     "rate": 0.89,
     "img_from": "img/euro.png",
     "img_to": "img/uk.png"
     },
    {"from": "eur",
     "to": "usd",
     "rate": 1.11,
     "img_from": "img/euro.png",
     "img_to": "img/usa.svg"
     },
    {"from": "usd",
     "to": "usd",
     "rate": 1.0,
     "img_from": "img/usa.svg",
     "img_to": "img/usa.svg"
     },
    {"from": "usd",
     "to": "gbp",
     "rate": 0.80,
     "img_from": "img/usa.svg",
     "img_to": "img/uk.png"
     },
    {"from": "usd",
     "to": "eur",
     "rate": 0.90,
     "img_from": "img/usa.svg",
     "img_to": "img/euro.png"
     }
]


# Create your views here.
def dashboard_page(request):
    try:
        data = {}
        if (request.user.is_authenticated):
            data["auth_user"] = request.user
            data["active_page"] = 'dashboard'
            return render(request, "payapp/dashboard.html", data)
        else:
            redirect("/login")

    except Exception as e:
        print("{}".format(str(e)))


def transfer_page(request):
    try:
        data = {}
        if (request.user.is_authenticated):
            data["auth_user"] = request.user
            data["active_page"] = 'transfer'
            return render(request, "payapp/transfer.html", data)
        else:
            redirect("/login")

    except Exception as e:
        print("{}".format(str(e)))


def transactions_page(request):
    try:
        data = {}
        if (request.user.is_authenticated):
            data["auth_user"] = request.user
            data["active_page"] = 'transactions'
            return render(request, "payapp/transactions.html", data)
        else:
            redirect("/login")

    except Exception as e:
        print("{}".format(str(e)))


def settings_page(request):
    try:
        data = {}
        if (request.user.is_authenticated):
            data["auth_user"] = request.user
            data["active_page"] = 'settings'
            data["currencies"] = Currency.objects.filter(is_active=True)
            data["rate_data"] = dumps(CONVERSION_RATE)
            data["static_url"] = os.path.join(settings.STATIC_URL)
            print(data)
            return render(request, "payapp/settings.html", data)
        else:
            redirect("/login")

    except Exception as e:
        print("{}".format(str(e)))


def conversion(request, currency_one, currency_two, amount):
    data = {
        "status": False,
        "msg": "Something went wrong"
    }
    try:
        currency_one = Currency.objects.filter(code=currency_one.lower()).first()
        currency_two = Currency.objects.filter(code=currency_two.lower()).first()
        amount = float(amount) if amount else 1.0
        converted_rate = None

        if currency_one is None or currency_two is None:
            data['msg'] = "We don't handle this currency"
            return JsonResponse(data, status=400)
        elif not amount or amount <= 0:
            data['msg'] = "Invalid amount"
            return JsonResponse(data, status=400)
        else:
            converted_rate = [rate for rate in CONVERSION_RATE if
                              rate["from"] == currency_one.code and rate["to"] == currency_two.code]
            if len(converted_rate) <= 0:
                data['msg'] = "we currently do not convert {} to {}".format(currency_one.upper(), currency_two.upper())
                return JsonResponse(data, status=400)
            else:
                converted_rate = converted_rate[0]
                converted_amount = converted_rate["rate"] * amount
                conversion_data = dict()

                conversion_data["currency_from"] = converted_rate["from"]
                conversion_data["currency_to"] = converted_rate["to"]
                conversion_data["amount"] = converted_amount

                data["status"] = True
                data["msg"] = "Converted successfully"
                data["data"] = conversion_data

        return JsonResponse(data, status=200)
    except Exception as e:
        print(e)
        data["msg"] = data["msg"] + "{}".format(str(e))
        return JsonResponse(data, status=500)
