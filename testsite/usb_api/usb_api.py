from models import *

class USB_API(object):
    @classmethod
    def process_message(cls,message,usb_hashed_uuid,session):
        try:
            valid_actions = {
                'username_exists':cls.username_exists,
                'register':cls.register,
                'login':cls.login,
                'edit_user_info':cls.edit_user_info,
                'get_user_info':cls.get_user_info,
                'logout':cls.logout,
            }

            action = message['action']
            data = message['data']

            return_data = valid_actions[action](data,usb_hashed_uuid,session,message)
            return return_data            
        except Exception, e:
            return {
                'success':False,
                'message':str(e),
                'query':message
            }

    @classmethod
    def username_exists(cls,data,usb_hashed_uuid,session,message):
        username = data['username']
        username_already_exists = USBUser.objects.filter(username=username).count() > 0
        return {
            'success':True,
            'message':username_already_exists,
            'query':message
        }  

    @classmethod
    def register(cls,data,usb_hashed_uuid,session,message):
        usbuser_obj = USBUser.objects.get(usb_code=usb_hashed_uuid)
        if usbuser_obj.is_registered():
            return {
                'success':False,
                'message':'User already registered',
                'query':message
            }

        if USBUser.objects.filter(username=data['username']).count() > 0:
            return {
                'success':False,
                'message':'Username already exists',
                'query':message
            }

        usbuser_obj.username = data['username'].lower()
        usbuser_obj.first_name = data['first_name']
        usbuser_obj.last_name = data['last_name']
        usbuser_obj.email = data['email']
        usbuser_obj.sex = data['sex']
        usbuser_obj.birthdate = data['birthdate']
        usbuser_obj.address = data.get('address',None)
        usbuser_obj.contact_number = data.get('contact_number',None)
        usbuser_obj.country = data.get('country',None)
        usbuser_obj.save()

        return {
            'success':False,
            'message':'Successfully registered user',
            'query':message
        }

    @classmethod
    def login(cls,data,usb_hashed_uuid,session,message):
        pass

    @classmethod
    def edit_user_info(cls,data,usb_hashed_uuid,session,message):
        pass

    @classmethod
    def get_user_info(cls,data,usb_hashed_uuid,session,message):
        pass

    @classmethod
    def logout(data,usb_hashed_uuid,session,message):
        pass
