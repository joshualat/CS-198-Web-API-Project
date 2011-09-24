import os.path, os
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from lib.ConsoleTools import *
from lib.SecTools import *
from lib.PKA import *
from lib.SKA import *
from usb_api import *
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
    return HttpResponse(SecTools.serialize("Invalid"))

@csrf_exempt
def transfer_shared_key(request):
    if request.method == 'POST':
        usb_hashed_uuid = request.POST.get('usb_hashed_uuid',None)
        encrypted_message_1 = request.POST.get('encrypted_message_1',None)
        encrypted_message_2 = request.POST.get('encrypted_message_2',None)

        if usb_hashed_uuid != None and encrypted_message_1 != None and encrypted_message_2 != None:  
            # obtain private key of website
            private_key_file = os.path.join(BOX_DIR,'private.key')
            private_key = ConsoleTools.file_read(private_key_file)

            # decrypt message
            message_1 = PKA.decrypt(private_key,encrypted_message_1.decode("ascii"))
            message_2 = PKA.decrypt(private_key,encrypted_message_2.decode("ascii"))

            if message_1['usb_hashed_uuid'] == usb_hashed_uuid:                
                # store data to appropriate usb user object
                usbuser_obj = USBUser.objects.get(usb_code=usb_hashed_uuid)
                usbuser_obj.shared_key = message_1['shared_key']
                if usbuser_obj.password_code == "" or usbuser_obj.password_code == None:
                    usbuser_obj.password_code = message_2['usb_hashed_password']
                elif usbuser_obj.password_code != message_2['usb_hashed_password']:
                    return HttpResponse("Invalid Password")                    
                usbuser_obj.salt = message_2['usb_salt']
                usbuser_obj.save()
                return HttpResponse("OK")
    return HttpResponse("Invalid")

@csrf_exempt
def secure_connection(request):
    if request.method == 'POST':
        usb_hashed_uuid = request.POST.get('usb_hashed_uuid',None)
        encrypted_message = request.POST.get('encrypted_message',None)

        if usb_hashed_uuid != None and encrypted_message != None:  
            usbuser_obj = USBUser.objects.get(usb_code=usb_hashed_uuid)
            shared_key = usbuser_obj.shared_key

            message_group = SKA.decrypt(shared_key,encrypted_message.decode("base64"))
            if message_group['usb_hashed_uuid'] == usb_hashed_uuid and message_group['usb_hashed_password'] == usbuser_obj.password_code:
                message = message_group['message']
                output = USB_API.process_message(message,usb_hashed_uuid,request.session)
                output = SecTools.serialize(output)
                return HttpResponse(output)
    return HttpResponse(SecTools.serialize("Invalid"))

@csrf_exempt
def test(request):
    if request.method == 'POST':
        message = 'POST:' + str(request.POST.get('message',None))
    elif request.method == 'GET':
        message = 'GET:' + str(request.GET.get('message',None))
    return HttpResponse(message+" :)")
