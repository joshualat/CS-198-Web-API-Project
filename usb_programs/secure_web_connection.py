from secure_file_io import *
from lib.ConsoleTools import *
from lib.ConnectTools import *
from lib.SecTools import *

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

    def __init__(self,url):
        url = url.lower()
        self.url = url
        url_data = SecureFileIO.load_url_data(url)
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
        return SecTools.generate_hash(uuid)

    def usb_salt(self):
        config = ConsoleTools.file_read('box/config')
        return config.split("\n")[1]

    def web_public_key(self):
        return self.public_key

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

    def transfer_shared_key(self):
        pass
