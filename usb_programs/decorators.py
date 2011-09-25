from getpass import getpass

ATTEMPTS = 3

def usb_login_first(function=None):
    def _dec(func): 
        def new_function(*args, **kwargs):
            if not login_usb(): return # return if login is unsuccessful
            print "HEY"
            func(*args, **kwargs)
         
        new_function.__name__ = func.__name__
        new_function.__dict__ = func.__dict__
        new_function.__doc__ = func.__doc__
         
        return new_function
    
    return _dec(function) if function else _dec
