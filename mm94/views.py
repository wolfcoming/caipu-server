from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def mmindex(request):
    return HttpResponse(u"欢迎mm")


