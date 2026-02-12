from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

# This view will intentionally create an error
def error_view(request):
    x = 10 / 0   # This will create ZeroDivisionError
    return HttpResponse("This will not run")
