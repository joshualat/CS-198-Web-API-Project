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
    def save_data(cls,path,data):
        """saves the data to <path>.data file"""
        data = SecTools.serialize(data)
        ConsoleTools.file_write(path + '.data',data)

    @classmethod
    def load_data(cls,path):        
        """loads the data from <path>.data file"""
        data = ConsoleTools.file_read(path + '.data')
        return SecTools.deserialize(data) if data else {}
        
    @classmethod
    def save_usb_data(cls,usb_data,path=''):
        """saves the usb data to usb.data file"""
        cls.save_data(path + 'box/usb', usb_data)

    @classmethod
    def load_usb_data(cls,path=''):        
        """loads the usb data from usb.data file"""
        return cls.load_data(path + 'box/usb')
        
    @classmethod
    def save_web_data(cls,web_data):
        """saves the web data to web.data file"""
        cls.save_data('box/web', web_data)

    @classmethod
    def load_web_data(cls):        
        """loads the web data from web.data file"""
        return cls.load_data('box/web')

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
    def update_usb_usernames(cls,url,username):
        """update the usb data stored in the usb.data file"""
        usb_data = cls.load_usb_data()
        if not usb_data.has_key('usernames'):
            usb_data['usernames'] = {}
        usb_data['usernames'][url] = username
        cls.save_usb_data(usb_data)
    
