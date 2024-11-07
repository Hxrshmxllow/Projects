from django.shortcuts import render
from django.http import HttpResponse

def users(request):
    print('here')
    return HttpResponse('Hello World!')