from django.urls import path
from .views import *



urlpatterns = [
    path('',homepage,name = 'home'),
    path('searchresult/',result, name = 'result'),
    path('download/',download,name="download"),

]