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

    """
    SecureWebConnection class

    Usable functions:
        save
        usb_public_key
        usb_private_key
        usb_hashed_uuid
        usb_salt
        usb_hashed_password
        web_public_key
        web_hashed_uuid
        exchange_keys
        generate_shared_key
        delete_shared_key
        transfer_shared_key
        start
        end
        secure_message
        secure_connection

    """

    def __init__(self,url,hashed_password):
        url = url.lower()
        self.url = url
        url_data = SecureFileIO.load_url_data(url)
        self.hashed_password = hashed_password.encode("base64")
        if url_data != None:
            self.hashed_uuid = url_data['hashed_uuid']
            self.public_key = url_data['public_key']
            self.shared_key = url_data['shared_key']

    def save(self):
        """updates the url data storage"""
        SecureFileIO.update_url_data(self.url,self.hashed_uuid,self.public_key,self.shared_key)

    @classmethod
    def usb_public_key(cls):
        """returns the public key of the USB"""
        return ConsoleTools.file_read('box/public.key')

    @classmethod
    def usb_private_key(cls):
        """returns the private key of the USB"""
        return ConsoleTools.file_read('box/private.key')

    @classmethod
    def usb_hashed_uuid(cls):
        """returns the hashed uuid of the USB"""
        config = ConsoleTools.file_read('box/config')
        uuid = config.split("\n")[0]
        return SecTools.generate_hash(uuid).encode("hex")
        
    @classmethod
    def usb_salt(cls):
        """returns the salt of the USB"""
        config = ConsoleTools.file_read('box/config')
        return config.split("\n")[1]

    def usb_hashed_password(self):
        """returns the hashed password of the user"""
        return self.hashed_password

    def web_public_key(self):
        """returns the public key of the website"""
        return self.public_key

    def web_hashed_uuid(self):
        """returns the hashed uuid of the website"""
        return self.hashed_uuid

    def exchange_keys(self):
        """sends a post request in order to exchange public keys with the website"""
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
        """returns a shared key; generates a new one if no shared key exists"""
        if self.shared_key == "":
            self.shared_key = SKA.generate_key()
            self.save()
        return self.shared_key

    def delete_shared_key(self):
        """delete current shared key"""
        self.shared_key = ""
        self.save()

    def transfer_shared_key(self):
        """sends a post request in order to transfer the shared key to the website"""
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
            "usb_hashed_uuid":str(self.usb_hashed_uuid()),
            "encrypted_message_1":str(encrypted_message_1),
            "encrypted_message_2":str(encrypted_message_2),
        }

        signature = PKA.sign(self.usb_private_key(),params)
        params['signature'] = signature

        page = ConnectTools.request_post(target_url,params)
        return page

    def start(self):
        """begin transactions with the website"""
        self.delete_shared_key()
        self.exchange_keys()
        self.generate_shared_key()
        return self.transfer_shared_key()

    def end(self):
        """end transactiosn with the website"""
        self.delete_shared_key()

    def secure_message(self,action, **kwargs):
        """wrapper function for secure connection"""
        return self.secure_connection({
            'action':action,
            'data':kwargs
        })
    
    def secure_connection(self,message=None):
        """sends a secured message to the website"""
        shared_key = self.generate_shared_key()
        message_group = {
            "usb_hashed_uuid":self.usb_hashed_uuid(),
            "usb_hashed_password":self.usb_hashed_password(),
            "message":message
        }
        encrypted_message = SKA.encrypt(shared_key,message_group)
        target_url = self.url + "usb/secure_connection"
        params = {
            "usb_hashed_uuid":self.usb_hashed_uuid(),
            "encrypted_message":encrypted_message.encode("base64"),
        }
        page = ConnectTools.request_post(target_url,params)
        if page == 'Invalid':
            return page

        page = SKA.decrypt(shared_key,page.decode("base64"))
        page = SecTools.deserialize(page)
        if message!=None and message.get('action',None) == 'login':
            login_url = ConnectTools.browser_open(self.url + "usb/login",page['message'])
            self.delete_shared_key()
        if message!=None and message.get('action',None) == 'logout':
            ConnectTools.browser_open(self.url + "usb/logout")
        return page
