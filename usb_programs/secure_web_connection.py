from secure_file_io import *
from lib.ConsoleTools import *
from lib.ConnectTools import *
from lib.SecTools import *
from lib.SKA import *
from lib.PKA import *

# Secure Web Connection Class
"""
from secure_web_connection import *
swc = SecureWebConnection("http://localhost:8000/")
swc.exchange_keys()
"""

class SecureWebConnection(object):

    url = "http://localhost:8000/"
    hashed_uuid = ""
    public_key = ""
    shared_key = ""
    hashed_password = ""

    def __init__(self,url,hashed_password):
        url = url.lower()
        self.url = url
        url_data = SecureFileIO.load_url_data(url)
        self.hashed_password = hashed_password
        if url_data != None:
            self.hashed_uuid = url_data['hashed_uuid']
            self.public_key = url_data['public_key']
            self.shared_key = url_data['shared_key']

    def save(self):
        SecureFileIO.update_url_data(self.url,self.hashed_uuid,self.public_key,self.shared_key)

    def usb_public_key(self):
        return ConsoleTools.file_read('box/public.key')

    def usb_private_key(self):
        return ConsoleTools.file_read('box/private.key')

    def usb_hashed_uuid(self):
        config = ConsoleTools.file_read('box/config')
        uuid = config.split("\n")[0]
        return SecTools.generate_hash(uuid).encode("base64")

    def usb_salt(self):
        config = ConsoleTools.file_read('box/config')
        return config.split("\n")[1]

    def usb_hashed_password(self):
        return self.hashed_password

    def web_public_key(self):
        return self.public_key

    def web_hashed_uuid(self):
        return self.hashed_uuid

    def exchange_keys(self):
        target_url = self.url + "usb/exchange_keys"
        params = {
            "usb_public_key":self.usb_public_key(),
            "usb_hashed_uuid":self.usb_hashed_uuid(),
        }
        page = ConnectTools.request_post(target_url,params)
        page = SecTools.deserialize(page)
        self.public_key = page['web_public_key']
        self.hashed_uuid = page['web_hashed_uuid']
        self.save()

    def generate_shared_key(self):
        if self.shared_key == "":
            self.shared_key = SKA.generate_key()
            self.save()
        return self.shared_key

    def delete_shared_key(self):
        self.shared_key = ""
        self.save()

    def transfer_shared_key(self):
        shared_key = self.generate_shared_key()
        message_1 = {
            "usb_hashed_uuid":self.usb_hashed_uuid(),
            "shared_key":shared_key
        }
        message_2 = {
            "usb_hashed_password":self.usb_hashed_password(),
            "usb_salt":self.usb_salt()
        }

        encrypted_message_1 = PKA.encrypt(self.web_public_key(),message_1)
        encrypted_message_2 = PKA.encrypt(self.web_public_key(),message_2)

        target_url = self.url + "usb/transfer_shared_key"
        params = {
            "usb_hashed_uuid":self.usb_hashed_uuid(),
            "encrypted_message_1":encrypted_message_1,
            "encrypted_message_2":encrypted_message_2,
        }

        page = ConnectTools.request_post(target_url,params)
        return page
