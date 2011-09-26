from lib.ConsoleTools import *
from lib.SecTools import *

class SecureFileIO(object):

    """
    SecureFileIO class

    Usable functions:
        save_web_data
        load_web_data
        update_url_data
        load_url_data
        save_usb_data
        load_usb_data

    """

    @classmethod
    def save_web_data(cls,web_data):
        """saves the web data to web.data file"""
        web_data = SecTools.serialize(web_data)
        ConsoleTools.file_write('box/web.data',web_data)

    @classmethod
    def load_web_data(cls):        
        """loads the web data from web.data file"""
        web_data = ConsoleTools.file_read('box/web.data')
        if web_data != None:
            web_data = SecTools.deserialize(web_data)
        else:
            web_data = {}
        return web_data

    @classmethod
    def update_url_data(cls,url,hashed_uuid,public_key,shared_key):
        """updates the web data stored in the web.data file"""
        web_data = cls.load_web_data()
        web_data[url] = {
            'hashed_uuid':hashed_uuid,
            'public_key':public_key,
            'shared_key':shared_key,
        }
        cls.save_web_data(web_data)

    @classmethod
    def load_url_data(cls,url):
        """loads the specific url data from the web.data file"""
        web_data = cls.load_web_data()
        return web_data.get(url,None)
        
        
    @classmethod
    def save_usb_data(cls,usb_data):
        """saves the usb data to usb.data file"""
        usb_data = SecTools.serialize(usb_data)
        ConsoleTools.file_write('box/usb.data',usb_data)

    @classmethod
    def load_usb_data(cls):        
        """loads the usb data from usb.data file"""
        usb_data = ConsoleTools.file_read('box/usb.data')
        return SecTools.deserialize(usb_data) if usb_data else {}
