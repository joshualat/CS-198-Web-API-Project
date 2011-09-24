import os.path, os
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from lib.ConsoleTools import *
from lib.SecTools import *
from lib.PKA import *
from models import *

BOX_DIR = os.path.join(settings.PROJECT_DIR,'usb_api','box')

def home(request):    
    """Introduction, Tutorials"""
    return HttpResponse("Home")

@csrf_exempt
def exchange_keys(request):
    if request.method == 'POST':
        # get hashed uuid and public key of usb
        usb_hashed_uuid = request.POST.get('usb_hashed_uuid',None)
        usb_public_key = request.POST.get('usb_public_key',None)

        if usb_hashed_uuid != None and usb_public_key != None:            

            # TODO: save usb_hashed_uuid and usb_public_key to db
            # check if account with usb_hashed_uuid exists
            usbuser_obj, created = USBUser.objects.get_or_create(usb_code=usb_hashed_uuid,defaults={'public_key':usb_public_key})
            
            # obtain hashed uuid of website
            config_file = os.path.join(BOX_DIR,'config')
            config = ConsoleTools.file_read(config_file)
            uuid = config.split("\n")[0]
            web_hashed_uuid = SecTools.generate_hash(uuid)

            # obtain public key of website
            public_key_file = os.path.join(BOX_DIR,'public.key')
            public_key = ConsoleTools.file_read(public_key_file)

            output = {'web_public_key':public_key,'web_hashed_uuid':web_hashed_uuid}
            output = SecTools.serialize(output)

            return HttpResponse(output)
    return HttpResponse("Invalid")

@csrf_exempt
def transfer_shared_key(request):
    if request.method == 'POST':
        usb_hashed_uuid = request.POST.get('usb_hashed_uuid',None)
        encrypted_message = request.POST.get('encrypted_message',None)

        if usb_hashed_uuid != None and encrypted_message != None:  
            # obtain private key of website
            private_key_file = os.path.join(BOX_DIR,'private.key')
            private_key = ConsoleTools.file_read(private_key_file)

            # decrypt message
            shared_key = PKA.decrypt(private_key,encrypted_message.decode("ascii"))
            usbuser_obj = USBUser.objects.get(usb_code=usb_hashed_uuid)
            usbuser_obj.shared_key = shared_key
            usbuser_obj.save()

            #output = message
            output = "OK"

            output = SecTools.serialize(output)
            return HttpResponse(output)
    return HttpResponse("Invalid")

@csrf_exempt
def secure_connection(request):
    if request.method == 'POST':
        pass
    return HttpResponse("Invalid")

@csrf_exempt
def test(request):
    if request.method == 'POST':
        message = 'POST:' + str(request.POST.get('message',None))
    elif request.method == 'GET':
        message = 'GET:' + str(request.GET.get('message',None))
    return HttpResponse(message+" :)")
