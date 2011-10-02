from lib.ConsoleTools import *
from lib.SecTools import *
from secure_file_io import *
from secure_web_connection import *
from getpass import getpass
import os

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

password = None
LOGIN_ATTEMPTS = 3

#decorators

def verify_first(function=None):
    ''' indicates that login must first be given'''
    def _dec(func): 
        def new_function(*args, **kwargs):
            path = kwargs['path'] if kwargs.has_key('path') else ''
            if not os.path.exists(path + 'box'):
                if path:
                    raise Exception('No usb account exists in ' + path + '.')
                else:
                    raise Exception('No usb account exists here.')
            return func(*args, **kwargs)
         
        new_function.__name__ = func.__name__
        new_function.__dict__ = func.__dict__
        new_function.__doc__ = func.__doc__
        
        return new_function
    
    return _dec(function) if function else _dec

def not_implemented(function=None):
    '''indicates that the function is not yet implemented'''
    def _dec(func): 
        def new_function(*args, **kwargs):
            raise NotImplementedError()
         
        new_function.__name__ = func.__name__
        new_function.__dict__ = func.__dict__
        new_function.__doc__ = func.__doc__
         
        return new_function
    
    return _dec(function) if function else _dec
    
    
#utilities

def pretty_print(page):
    ''' Prints HTTP response from secure_connection '''
    if isinstance(page, dict):
        print page['query']['action'], ['failed', 'succeeded'][page['success']]
        print 'Message:', page['message']
        print
    else:
        print page

def set_password(new_pass):
    global password
    password = new_pass

def hashed_password(path=''):
    return ConsoleTools.file_read(path + 'box/hashedpass')

def connect(input=False):
    ''' Create a SecureWebConnection by inputting url and password '''
    url = url_input() if input else url_choose()
    if not url:
        raise Exception('No registered websites.')
    return SecureWebConnection(url, hashed_password())
    
def login(message=''):
    ''' gather password '''
    global password
    if password: return True
    
    if message:
        message = 'Enter ' + message + ' password: '
    else:
        message = 'Enter password: '
    for i in range(1, LOGIN_ATTEMPTS + 1):
        password = getpass(message)
        if password: return True # if nonempty.
        if i == 1:
            message = 'Try again. ' + message
    print 'Attempts used up.'
    return False

def usb_data_for_site(url=None):
    usb_data = SecureFileIO.load_usb_data()
    if usb_data.has_key('usernames'):
        if url and usb_data['usernames'].has_key(url):
            usb_data['username'] = usb_data['usernames'][url]
        usb_data.pop('usernames')
    return usb_data

def input_password(msg = 'Enter password'):
    '''gets new password from user two times.'''
    while True:
        pass1 = getpass(msg + ': ')
        pass2 = getpass(msg + ' (again): ')
        if not (len(pass1) and len(pass2)):
            print "Please input the password twice."
            continue
        if pass1 == pass2: return pass1
        print "Passwords didn't match."
        
def url_input():
    ''' asks a valid url from the user '''
    return ConsoleTools.accept_input("Please enter url: ")#just a normal input for now

def get_sites():
    web_data = SecureFileIO.load_usb_data()
    return web_data['usernames'].keys() if web_data.has_key('usernames') else []
    
def url_choose():
    '''choose from websites written in drive'''
    web_data = get_sites()
    
    if not web_data:
        print 'No registered sites'
        return None
        
    choices = {}
    size = 0
    
    for website in web_data.keys():
        size = size + 1
        choices[str(size)] = website
    
    print 'Registered sites:'
    for index, website in choices.items():
        print '(' + index + ')', website
    
    choice = ConsoleTools.accept_input('Select website', choices.keys())
    
    return choices[choice];