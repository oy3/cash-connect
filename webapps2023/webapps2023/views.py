from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect


def home_page(request):
    return render(request, "home/index.html")
