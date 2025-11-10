from django.shortcuts import render

# Create your views here.
def subapp(request):
    return render(request,'subapp/subapps.html')

def login(request):
    return render(request,'subapp/login.html')