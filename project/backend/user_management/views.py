from django.shortcuts import render
from django.http import HttpResponse

def register(request):
    return HttpResponse("Hello, world. You're at the user_management register.")