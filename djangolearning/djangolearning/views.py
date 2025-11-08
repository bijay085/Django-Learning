from django.http import HttpResponse
from django.shortcuts import render

def home(request):
    # return HttpResponse("Hello from django views, and hompepage")
    return render(request,'website/index.html')

def about(request):
    return HttpResponse("Hello from django views, and about page")

def contact(request):
    return HttpResponse("Hello from django views, and contact page")