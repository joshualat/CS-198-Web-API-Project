from django.http import HttpResponse

def home(request):    
    """Introduction, Tutorials"""
    return HttpResponse("Home")
