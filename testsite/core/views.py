from django.http import HttpResponse
from testsite.usb_api.decorators import usb_login_required
from testsite.usb_api.models import *

@usb_login_required
def index(request):
    usbuser_obj = USBUser.objects.get(usb_code=request.session['usb_code'])
    sample_output_dict = {
        'username':usbuser_obj.username,
        'first_name':usbuser_obj.first_name,
        'last_name':usbuser_obj.last_name,
        'email':usbuser_obj.email,
        'sex':usbuser_obj.sex,
    }
    sample_output = ""
    for output in sample_output_dict:
        sample_output += str(output) + ": " + str(sample_output_dict[output]) + "<br />"
    return HttpResponse(sample_output)
