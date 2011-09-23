from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

def home(request):    
    """Introduction, Tutorials"""
    return HttpResponse("Home")

@csrf_exempt
def test(request):
    if request.method == 'POST':
        message = 'POST:' + str(request.POST.get('message',None))
    elif request.method == 'GET':
        message = 'GET:' + str(request.GET.get('message',None))
    return HttpResponse(message+" :)")
