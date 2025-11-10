from django.urls import path
from . import views

# localhoost:8000/subapp
# localhoost:8000/subapp/login
urlpatterns = [
    path('', views.subapp, name='subapphomepage'),
    path('login', views.login, name='login'),
]
