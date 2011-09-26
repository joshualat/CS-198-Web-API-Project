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

def login_first(function=None):
    ''' indicates that login must first be given'''
    def _dec(func): 
        def new_function(*args, **kwargs):
            if not login(): return # return if login is unsuccessful
            return func(*args, **kwargs)
         
        new_function.__name__ = func.__name__
        new_function.__dict__ = func.__dict__
        new_function.__doc__ = func.__doc__
         
        return new_function
    
    return _dec(function) if function else _dec

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

def set_password(new_pass):
    global password
    password = new_pass

@login_first
def hashed_password():
    return SecTools.generate_hash(password,SecureWebConnection.usb_salt())

def connect(input=False):
    url = url_input() if input else url_choose()
    if not url:
        raise Exception('No registered websites.')
    return SecureWebConnection(url, hashed_password())
    
def login():
    '''gathers password for reading of usb data'''
    global password
    
    if password: return True
    message = 'Enter USB password: '
    for i in range(1, LOGIN_ATTEMPTS + 1):
        password = getpass(message)
        if password: return True # if nonempty.
        message = 'Try again. Enter USB password: '
    print 'Attempts used up.'
    return False

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

def url_choose():
    '''choose from websites written in drive'''
    web_data = SecureFileIO.load_web_data()
    
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