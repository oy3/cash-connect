from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.conf import settings
from currency.models import Currency
from authy.models import UserWallet, Transaction
from json import dumps
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
import requests
from datetime import datetime, timedelta
from django.db import transaction as atomic_transaction

import os

User = get_user_model()


def get_countries(request):
    countries = [
        {"name": 'Afghanistan', "code": 'AF'},
        {"name": 'Åland Islands', "code": 'AX'},
        {"name": 'Albania', "code": 'AL'},
        {"name": 'Algeria', "code": 'DZ'},
        {"name": 'American Samoa', "code": 'AS'},
        {"name": 'AndorrA', "code": 'AD'},
        {"name": 'Angola', "code": 'AO'},
        {"name": 'Anguilla', "code": 'AI'},
        {"name": 'Antarctica', "code": 'AQ'},
        {"name": 'Antigua and Barbuda', "code": 'AG'},
        {"name": 'Argentina', "code": 'AR'},
        {"name": 'Armenia', "code": 'AM'},
        {"name": 'Aruba', "code": 'AW'},
        {"name": 'Australia', "code": 'AU'},
        {"name": 'Austria', "code": 'AT'},
        {"name": 'Azerbaijan', "code": 'AZ'},
        {"name": 'Bahamas', "code": 'BS'},
        {"name": 'Bahrain', "code": 'BH'},
        {"name": 'Bangladesh', "code": 'BD'},
        {"name": 'Barbados', "code": 'BB'},
        {"name": 'Belarus', "code": 'BY'},
        {"name": 'Belgium', "code": 'BE'},
        {"name": 'Belize', "code": 'BZ'},
        {"name": 'Benin', "code": 'BJ'},
        {"name": 'Bermuda', "code": 'BM'},
        {"name": 'Bhutan', "code": 'BT'},
        {"name": 'Bolivia', "code": 'BO'},
        {"name": 'Bosnia and Herzegovina', "code": 'BA'},
        {"name": 'Botswana', "code": 'BW'},
        {"name": 'Bouvet Island', "code": 'BV'},
        {"name": 'Brazil', "code": 'BR'},
        {"name": 'British Indian Ocean Territory', "code": 'IO'},
        {"name": 'Brunei Darussalam', "code": 'BN'},
        {"name": 'Bulgaria', "code": 'BG'},
        {"name": 'Burkina Faso', "code": 'BF'},
        {"name": 'Burundi', "code": 'BI'},
        {"name": 'Cambodia', "code": 'KH'},
        {"name": 'Cameroon', "code": 'CM'},
        {"name": 'Canada', "code": 'CA'},
        {"name": 'Cape Verde', "code": 'CV'},
        {"name": 'Cayman Islands', "code": 'KY'},
        {"name": 'Central African Republic', "code": 'CF'},
        {"name": 'Chad', "code": 'TD'},
        {"name": 'Chile', "code": 'CL'},
        {"name": 'China', "code": 'CN'},
        {"name": 'Christmas Island', "code": 'CX'},
        {"name": 'Cocos (Keeling) Islands', "code": 'CC'},
        {"name": 'Colombia', "code": 'CO'},
        {"name": 'Comoros', "code": 'KM'},
        {"name": 'Congo', "code": 'CG'},
        {"name": 'Congo, The Democratic Republic of the', "code": 'CD'},
        {"name": 'Cook Islands', "code": 'CK'},
        {"name": 'Costa Rica', "code": 'CR'},
        {"name": 'Cote D\'Ivoire', "code": 'CI'},
        {"name": 'Croatia', "code": 'HR'},
        {"name": 'Cuba', "code": 'CU'},
        {"name": 'Cyprus', "code": 'CY'},
        {"name": 'Czech Republic', "code": 'CZ'},
        {"name": 'Denmark', "code": 'DK'},
        {"name": 'Djibouti', "code": 'DJ'},
        {"name": 'Dominica', "code": 'DM'},
        {"name": 'Dominican Republic', "code": 'DO'},
        {"name": 'Ecuador', "code": 'EC'},
        {"name": 'Egypt', "code": 'EG'},
        {"name": 'El Salvador', "code": 'SV'},
        {"name": 'Equatorial Guinea', "code": 'GQ'},
        {"name": 'Eritrea', "code": 'ER'},
        {"name": 'Estonia', "code": 'EE'},
        {"name": 'Ethiopia', "code": 'ET'},
        {"name": 'Falkland Islands (Malvinas)', "code": 'FK'},
        {"name": 'Faroe Islands', "code": 'FO'},
        {"name": 'Fiji', "code": 'FJ'},
        {"name": 'Finland', "code": 'FI'},
        {"name": 'France', "code": 'FR'},
        {"name": 'French Guiana', "code": 'GF'},
        {"name": 'French Polynesia', "code": 'PF'},
        {"name": 'French Southern Territories', "code": 'TF'},
        {"name": 'Gabon', "code": 'GA'},
        {"name": 'Gambia', "code": 'GM'},
        {"name": 'Georgia', "code": 'GE'},
        {"name": 'Germany', "code": 'DE'},
        {"name": 'Ghana', "code": 'GH'},
        {"name": 'Gibraltar', "code": 'GI'},
        {"name": 'Greece', "code": 'GR'},
        {"name": 'Greenland', "code": 'GL'},
        {"name": 'Grenada', "code": 'GD'},
        {"name": 'Guadeloupe', "code": 'GP'},
        {"name": 'Guam', "code": 'GU'},
        {"name": 'Guatemala', "code": 'GT'},
        {"name": 'Guernsey', "code": 'GG'},
        {"name": 'Guinea', "code": 'GN'},
        {"name": 'Guinea-Bissau', "code": 'GW'},
        {"name": 'Guyana', "code": 'GY'},
        {"name": 'Haiti', "code": 'HT'},
        {"name": 'Heard Island and Mcdonald Islands', "code": 'HM'},
        {"name": 'Holy See (Vatican City State)', "code": 'VA'},
        {"name": 'Honduras', "code": 'HN'},
        {"name": 'Hong Kong', "code": 'HK'},
        {"name": 'Hungary', "code": 'HU'},
        {"name": 'Iceland', "code": 'IS'},
        {"name": 'India', "code": 'IN'},
        {"name": 'Indonesia', "code": 'ID'},
        {"name": 'Iran, Islamic Republic Of', "code": 'IR'},
        {"name": 'Iraq', "code": 'IQ'},
        {"name": 'Ireland', "code": 'IE'},
        {"name": 'Isle of Man', "code": 'IM'},
        {"name": 'Israel', "code": 'IL'},
        {"name": 'Italy', "code": 'IT'},
        {"name": 'Jamaica', "code": 'JM'},
        {"name": 'Japan', "code": 'JP'},
        {"name": 'Jersey', "code": 'JE'},
        {"name": 'Jordan', "code": 'JO'},
        {"name": 'Kazakhstan', "code": 'KZ'},
        {"name": 'Kenya', "code": 'KE'},
        {"name": 'Kiribati', "code": 'KI'},
        {"name": 'Korea, Democratic People\'S Republic of', "code": 'KP'},
        {"name": 'Korea, Republic of', "code": 'KR'},
        {"name": 'Kuwait', "code": 'KW'},
        {"name": 'Kyrgyzstan', "code": 'KG'},
        {"name": 'Lao People\'S Democratic Republic', "code": 'LA'},
        {"name": 'Latvia', "code": 'LV'},
        {"name": 'Lebanon', "code": 'LB'},
        {"name": 'Lesotho', "code": 'LS'},
        {"name": 'Liberia', "code": 'LR'},
        {"name": 'Libyan Arab Jamahiriya', "code": 'LY'},
        {"name": 'Liechtenstein', "code": 'LI'},
        {"name": 'Lithuania', "code": 'LT'},
        {"name": 'Luxembourg', "code": 'LU'},
        {"name": 'Macao', "code": 'MO'},
        {"name": 'Macedonia, The Former Yugoslav Republic of', "code": 'MK'},
        {"name": 'Madagascar', "code": 'MG'},
        {"name": 'Malawi', "code": 'MW'},
        {"name": 'Malaysia', "code": 'MY'},
        {"name": 'Maldives', "code": 'MV'},
        {"name": 'Mali', "code": 'ML'},
        {"name": 'Malta', "code": 'MT'},
        {"name": 'Marshall Islands', "code": 'MH'},
        {"name": 'Martinique', "code": 'MQ'},
        {"name": 'Mauritania', "code": 'MR'},
        {"name": 'Mauritius', "code": 'MU'},
        {"name": 'Mayotte', "code": 'YT'},
        {"name": 'Mexico', "code": 'MX'},
        {"name": 'Micronesia, Federated States of', "code": 'FM'},
        {"name": 'Moldova, Republic of', "code": 'MD'},
        {"name": 'Monaco', "code": 'MC'},
        {"name": 'Mongolia', "code": 'MN'},
        {"name": 'Montserrat', "code": 'MS'},
        {"name": 'Morocco', "code": 'MA'},
        {"name": 'Mozambique', "code": 'MZ'},
        {"name": 'Myanmar', "code": 'MM'},
        {"name": 'Namibia', "code": 'NA'},
        {"name": 'Nauru', "code": 'NR'},
        {"name": 'Nepal', "code": 'NP'},
        {"name": 'Netherlands', "code": 'NL'},
        {"name": 'Netherlands Antilles', "code": 'AN'},
        {"name": 'New Caledonia', "code": 'NC'},
        {"name": 'New Zealand', "code": 'NZ'},
        {"name": 'Nicaragua', "code": 'NI'},
        {"name": 'Niger', "code": 'NE'},
        {"name": 'Nigeria', "code": 'NG'},
        {"name": 'Niue', "code": 'NU'},
        {"name": 'Norfolk Island', "code": 'NF'},
        {"name": 'Northern Mariana Islands', "code": 'MP'},
        {"name": 'Norway', "code": 'NO'},
        {"name": 'Oman', "code": 'OM'},
        {"name": 'Pakistan', "code": 'PK'},
        {"name": 'Palau', "code": 'PW'},
        {"name": 'Palestinian Territory, Occupied', "code": 'PS'},
        {"name": 'Panama', "code": 'PA'},
        {"name": 'Papua New Guinea', "code": 'PG'},
        {"name": 'Paraguay', "code": 'PY'},
        {"name": 'Peru', "code": 'PE'},
        {"name": 'Philippines', "code": 'PH'},
        {"name": 'Pitcairn', "code": 'PN'},
        {"name": 'Poland', "code": 'PL'},
        {"name": 'Portugal', "code": 'PT'},
        {"name": 'Puerto Rico', "code": 'PR'},
        {"name": 'Qatar', "code": 'QA'},
        {"name": 'Reunion', "code": 'RE'},
        {"name": 'Romania', "code": 'RO'},
        {"name": 'Russian Federation', "code": 'RU'},
        {"name": 'RWANDA', "code": 'RW'},
        {"name": 'Saint Helena', "code": 'SH'},
        {"name": 'Saint Kitts and Nevis', "code": 'KN'},
        {"name": 'Saint Lucia', "code": 'LC'},
        {"name": 'Saint Pierre and Miquelon', "code": 'PM'},
        {"name": 'Saint Vincent and the Grenadines', "code": 'VC'},
        {"name": 'Samoa', "code": 'WS'},
        {"name": 'San Marino', "code": 'SM'},
        {"name": 'Sao Tome and Principe', "code": 'ST'},
        {"name": 'Saudi Arabia', "code": 'SA'},
        {"name": 'Senegal', "code": 'SN'},
        {"name": 'Serbia and Montenegro', "code": 'CS'},
        {"name": 'Seychelles', "code": 'SC'},
        {"name": 'Sierra Leone', "code": 'SL'},
        {"name": 'Singapore', "code": 'SG'},
        {"name": 'Slovakia', "code": 'SK'},
        {"name": 'Slovenia', "code": 'SI'},
        {"name": 'Solomon Islands', "code": 'SB'},
        {"name": 'Somalia', "code": 'SO'},
        {"name": 'South Africa', "code": 'ZA'},
        {"name": 'South Georgia and the South Sandwich Islands', "code": 'GS'},
        {"name": 'Spain', "code": 'ES'},
        {"name": 'Sri Lanka', "code": 'LK'},
        {"name": 'Sudan', "code": 'SD'},
        {"name": 'Suriname', "code": 'SR'},
        {"name": 'Svalbard and Jan Mayen', "code": 'SJ'},
        {"name": 'Swaziland', "code": 'SZ'},
        {"name": 'Sweden', "code": 'SE'},
        {"name": 'Switzerland', "code": 'CH'},
        {"name": 'Syrian Arab Republic', "code": 'SY'},
        {"name": 'Taiwan, Province of China', "code": 'TW'},
        {"name": 'Tajikistan', "code": 'TJ'},
        {"name": 'Tanzania, United Republic of', "code": 'TZ'},
        {"name": 'Thailand', "code": 'TH'},
        {"name": 'Timor-Leste', "code": 'TL'},
        {"name": 'Togo', "code": 'TG'},
        {"name": 'Tokelau', "code": 'TK'},
        {"name": 'Tonga', "code": 'TO'},
        {"name": 'Trinidad and Tobago', "code": 'TT'},
        {"name": 'Tunisia', "code": 'TN'},
        {"name": 'Turkey', "code": 'TR'},
        {"name": 'Turkmenistan', "code": 'TM'},
        {"name": 'Turks and Caicos Islands', "code": 'TC'},
        {"name": 'Tuvalu', "code": 'TV'},
        {"name": 'Uganda', "code": 'UG'},
        {"name": 'Ukraine', "code": 'UA'},
        {"name": 'United Arab Emirates', "code": 'AE'},
        {"name": 'United Kingdom', "code": 'GB'},
        {"name": 'United States', "code": 'US'},
        {"name": 'United States Minor Outlying Islands', "code": 'UM'},
        {"name": 'Uruguay', "code": 'UY'},
        {"name": 'Uzbekistan', "code": 'UZ'},
        {"name": 'Vanuatu', "code": 'VU'},
        {"name": 'Venezuela', "code": 'VE'},
        {"name": 'Viet Nam', "code": 'VN'},
        {"name": 'Virgin Islands, British', "code": 'VG'},
        {"name": 'Virgin Islands, U.S.', "code": 'VI'},
        {"name": 'Wallis and Futuna', "code": 'WF'},
        {"name": 'Western Sahara', "code": 'EH'},
        {"name": 'Yemen', "code": 'YE'},
        {"name": 'Zambia', "code": 'ZM'},
        {"name": 'Zimbabwe', "code": 'ZW'}
    ]

    return JsonResponse({"countries": countries})


# Create your views here.
def dashboard_page(request):
    try:
        data = {}
        if request.user.is_authenticated:
            data["auth_user"] = request.user
            data["wallet"] = UserWallet.objects.filter(user=request.user).first()
            if str(data["wallet"].currency) == "US Dollars":
                data["currency_code"] = "usd"
            elif str(data["wallet"].currency) == "GB Pounds":
                data["currency_code"] = "gbp"
            elif str(data["wallet"].currency) == "Euros":
                data["currency_code"] = "eur"
            else:
                data["currency_code"] = "n/a"

            data["active_page"] = 'dashboard'

            data["transactions"] = Transaction.objects.filter(Q(sent_from=request.user) | Q(sent_to=request.user)).order_by('-status')
            data["pending_transactions"] = Transaction.objects.filter(Q(sent_from=request.user) | Q(sent_to=request.user), status='pending').order_by('-transaction_date')
            data["success_transactions"] = Transaction.objects.filter(Q(sent_from=request.user) | Q(sent_to=request.user), status='completed').order_by('-transaction_date')
            data["other_transactions"] = Transaction.objects.filter(Q(sent_from=request.user) | Q(sent_to=request.user)).exclude(status='pending').order_by('-transaction_date')

            return render(request, "payapp/dashboard.html", data)
        else:
            redirect("/login")

    except Exception as e:
        print("{}".format(str(e)))
        redirect("/login")


def transfer_page(request, status='', msg=''):
    try:
        data = {}
        if request.user.is_authenticated:
            data["auth_user"] = request.user
            data["wallet"] = UserWallet.objects.filter(user=request.user).first()
            if str(data["wallet"].currency) == "US Dollars":
                data["currency_code"] = "usd"
            elif str(data["wallet"].currency) == "GB Pounds":
                data["currency_code"] = "gbp"
            elif str(data["wallet"].currency) == "Euros":
                data["currency_code"] = "eur"
            else:
                data["currency_code"] = "n/a"

            data["active_page"] = 'transfer'

            if status == 'success':
                data['error'] = True
                data['alert'] = False
                data['error_msg'] = msg
            elif status == 'failed':
                data['error'] = True
                data['alert'] = True
                data['error_msg'] = msg
            else:
                data['error'] = False

            print(data)
            print(status)
            print(msg)
            return render(request, "payapp/transfer.html", data)
        else:
            redirect("/login")

    except Exception as e:
        print("{}".format(str(e)))


def transactions_page(request):
    try:
        data = {}
        if request.user.is_authenticated:
            data["auth_user"] = request.user
            data["wallet"] = UserWallet.objects.filter(user=request.user).first()
            if str(data["wallet"].currency) == "US Dollars":
                data["currency_code"] = "usd"
            elif str(data["wallet"].currency) == "GB Pounds":
                data["currency_code"] = "gbp"
            elif str(data["wallet"].currency) == "Euros":
                data["currency_code"] = "eur"
            else:
                data["currency_code"] = "n/a"

            data["transactions"] = Transaction.objects.filter(Q(sent_from=request.user) | Q(sent_to=request.user)).order_by('-status')
            data["pending_transactions"] = Transaction.objects.filter(Q(sent_from=request.user) | Q(sent_to=request.user), status='pending').order_by('-transaction_date')
            data["success_transactions"] = Transaction.objects.filter(Q(sent_from=request.user) | Q(sent_to=request.user), status='completed').order_by('-transaction_date')
            data["other_transactions"] = Transaction.objects.filter(Q(sent_from=request.user) | Q(sent_to=request.user)).exclude(status='pending').order_by('-transaction_date')

            data["active_page"] = 'transactions'
            return render(request, "payapp/transactions.html", data)
        else:
            redirect("/login")

    except Exception as e:
        print("{}".format(str(e)))


def settings_page(request):
    try:
        data = {}
        if request.user.is_authenticated:
            data["auth_user"] = request.user
            data["active_page"] = 'settings'
            data["currencies"] = Currency.objects.filter(is_active=True)
            data["rate_data"] = dumps(settings.CONVERSION_RATE)
            data["static_url"] = os.path.join(settings.STATIC_URL)

            return render(request, "payapp/settings.html", data)
        else:
            redirect("/login")

    except Exception as e:
        print("{}".format(str(e)))


def help_page(request):
    try:
        data = {}
        if request.user.is_authenticated:
            data["auth_user"] = request.user
            data["active_page"] = 'help'
            data["static_url"] = os.path.join(settings.STATIC_URL)

            return render(request, "payapp/help.html", data)
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
            converted_rate = [rate for rate in settings.CONVERSION_RATE if
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
                conversion_data["rate"] = converted_rate["rate"]

                data["status"] = True
                data["msg"] = "Converted successfully"
                data["data"] = conversion_data

        return JsonResponse(data, status=200)
    except Exception as e:
        print(e)
        data["msg"] = data["msg"] + "{}".format(str(e))
        return JsonResponse(data, status=500)


@login_required
def update_profile(request):
    try:
        data = {}
        if request.method == 'POST':
            user = request.user
            user.first_name = request.POST.get('firstNameInput').capitalize()
            user.last_name = request.POST.get('lastNameInput').capitalize()
            # user.email = request.POST.get('emailInput').lower()
            user.phone = request.POST.get('phoneInput')
            user.address = request.POST.get('addressInput').capitalize()
            user.zipcode = request.POST.get('zipInput').upper()
            user.city = request.POST.get('cityInput').capitalize()
            user.state = request.POST.get('stateInput').capitalize()
            user.country = request.POST.get('countryInput')

            # Check for email
            if '@' not in user.email:
                data['error'] = True
                data['alert'] = True
                data['error_msg'] = "Invalid email address"

                return render(request, 'payapp/settings.html', data)

            user.save()
            data['error'] = True
            data['alert'] = False
            data['error_msg'] = "Your profile has been updated successfully."

            return redirect('/app/settings')
            # return render(request, 'payapp/settings.html', data)

        else:
            data['error'] = True
            data['alert'] = True
            data['error_msg'] = "Error while trying to update profile"
            return render(request, 'payapp/settings.html', data)

    except Exception as e:
        print("{}".format(str(e)))


@csrf_exempt
@login_required
def search_user(request):
    data = {
        "status": False,
        "msg": "Something went wrong"
    }

    print(request.method)

    try:
        if request.method == 'POST' and request.user.is_authenticated:
            print(request.POST)
            search = request.POST.get('search_user')
            qs = User.objects.filter(Q(email=search) | Q(username=search))

            if search is None or search == '' or not search:
                data["msg"] = "No search input provided"
                print(data)
                return JsonResponse(data, status=400)
            elif not qs.exists():
                data["msg"] = "User not found"
                print(data)
                return JsonResponse(data, status=400)
            elif qs.exists() and qs.first().username == request.user.username:
                data["msg"] = "User not found"
                print(data)
                return JsonResponse(data, status=400)
            else:
                data["msg"] = True
                data["msg"] = "User exists"
                data["data"] = model_to_dict(qs.first())
                return JsonResponse(data, status=200)
        else:
            redirect("/login")

    except Exception as e:
        print(e)
        data["msg"] = data["msg"] + "{}".format(str(e))
        return JsonResponse(data, status=500)


@login_required
@atomic_transaction.atomic
def create_transaction(request):
    try:
        data = {}
        if request.method == 'POST' and request.user.is_authenticated:
            user_wallet_sender_qs = UserWallet.objects.filter(user=request.user)
            sender = request.user
            receiver = request.POST.get('sent_to')
            receiver_user = User.objects.filter(username=receiver)
            user_wallet_receiver_qs = UserWallet.objects.filter(user=receiver_user.first()) if receiver_user is not None and receiver_user.exists() else None
            currency_from = user_wallet_sender_qs.first().currency if user_wallet_sender_qs is not None and user_wallet_sender_qs.exists() else None
            currency_to = user_wallet_receiver_qs.first().currency if user_wallet_receiver_qs is not None and user_wallet_receiver_qs.exists() else None
            amount_from = request.POST.get('amountInput')
            remark = request.POST.get('refInput')

            if receiver is None or not receiver or receiver_user is None or not receiver_user.exists():
                data['error'] = True
                data['alert'] = True
                data['error_msg'] = "Beneficiary not found"
                return render(request, "payapp/transfer.html", data)
            elif not amount_from:
                data['error'] = True
                data['alert'] = True
                data['error_msg'] = "Amount can not be empty"
                return render(request, "payapp/transfer.html", data)
            elif user_wallet_sender_qs.exists() and float(user_wallet_sender_qs.first().balance) < float(amount_from):
                data['error'] = True
                data['alert'] = True
                data['error_msg'] = "Insufficient funds"
                return render(request, "payapp/transfer.html", data)
                # return redirect("/app/transfer")
            else:
                with atomic_transaction.atomic():
                    response = requests.get("http://{}/conversion/{}/{}/{}".format(request.get_host(), currency_from.code, currency_to.code, amount_from))
                    response_data = response.json()
                    data = response_data.get("data", dict())
                    amount_to = data.get("amount", 0)
                    rate = data.get("rate", 0)

                    user_wallet_sender_qs.first().withdraw(amount_from)
                    user_wallet_receiver_qs.first().deposit(amount_to)

                    transaction = Transaction.objects.create(
                        sent_from=sender,
                        sent_to=receiver_user.first(),
                        currency_from=currency_from,
                        currency_to=currency_to,
                        amount_from=amount_from,
                        amount_to=amount_to,
                        rate=rate,
                        remark=remark
                    )

                    transaction.status = "completed"
                    transaction.save()

                    return redirect('/app/transfer', status='success', msg='Money sent successfully')
                    # return render(request, "payapp/transfer.html", data)
        else:
            redirect("/login")

    except Exception as e:
        print("{}".format(str(e)))


@login_required
@atomic_transaction.atomic
def request_money(request):
    try:
        data = {}
        if request.method == 'POST' and request.user.is_authenticated:
            receiver_wallet_qs = UserWallet.objects.filter(user=request.user)
            receiver = request.user
            sender = request.POST.get('req_from')
            sender_user = User.objects.filter(username=sender)
            sender_wallet_qs = UserWallet.objects.filter(user=sender_user.first()) if sender_user is not None and sender_user.exists() else None
            currency_from = sender_wallet_qs.first().currency if sender_wallet_qs is not None and sender_wallet_qs.exists() else None
            currency_to = receiver_wallet_qs.first().currency if receiver_wallet_qs is not None and receiver_wallet_qs.exists() else None
            amount_to = request.POST.get('reqAmountInput')
            remark = request.POST.get('reqRef')
            if sender is None or not sender or sender_user is None or not sender_user.exists():
                data['error'] = True
                data['alert'] = True
                data['error_msg'] = "Sender not found"

                # data['display_modal'] = True
                return render(request, "payapp/transfer.html", data)
            elif not amount_to:
                data['error'] = True
                data['alert'] = True
                data['error_msg'] = "Amount can not be empty"

                # data['display_modal'] = True
                return render(request, "payapp/transfer.html", data)
            else:
                with atomic_transaction.atomic():
                    response = requests.get("http://{}/conversion/{}/{}/{}".format(request.get_host(), currency_to.code, currency_from.code, amount_to))
                    response_data = response.json()
                    data = response_data.get("data", dict())
                    amount_from = data.get("amount", 0)
                    rate = data.get("rate", 0)

                    # user_wallet_sender_qs.first().withdraw(amount_from)
                    # user_wallet_receiver_qs.first().deposit(amount_to)

                    transaction = Transaction.objects.create(
                        sent_from=sender_user.first(),
                        sent_to=receiver,
                        currency_from=currency_from,
                        currency_to=currency_to,
                        amount_from=amount_from,
                        amount_to=amount_to,
                        rate=rate,
                        remark=remark
                    )
                    transaction.status = "pending"
                    transaction.save()

                    # data['display_modal'] = True
                    return redirect('/app/transfer', status='success', msg='Money request sent successfully')
                    # return render(request, "payapp/request.html", data)
        else:
            redirect("/login")

    except Exception as e:
        print("{}".format(str(e)))

