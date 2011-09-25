import sys 
from secure_web_connection import *
from util import *


required = {
    'username': ('user name', ()),
    'first_name': ('first name', ()),
    'last_name': ('last name', ()),
    'email': ('e-mail address', ()),
    'sex': ('sex', GENDER_CHOICES),
    'birthdate': ('birth date', ()),
}
optional = {
    'address': ('address', ()),
    'contact_number': ('contact number', ()),
    'country': ('country', ()),
}

'''
    #bogo fields
    usb_code = models.CharField(max_length=1000)
    password_code = models.CharField(max_length=1000)
    shared_key = models.CharField(max_length=1000)
    public_key = models.CharField(max_length=1000)
    salt = models.CharField(max_length=100)
    one_time_password = models.CharField(max_length=1000)

    #required fields
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    sex = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthdate = models.DateTimeField()

    #optional fields
    address = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    '''
    
@login_first
def edit_info():
    '''edits user information stored on usb drive '''
    #get data from disk
    #edit all fields
    #if field is optional, ask if edit is wanted (or make a mechanism on how to leave it unchanged)
    #save data to disk
    pass

@login_first
def update_info(target_conn=None):
    '''updates user information stored to website '''
    if not target_conn:
        target_conn=SecureWebConnection(url_choose(), hashed_password())
    target_conn.secure_message('edit_
    #send to website
    
    
def info(off=1):
    try:
        if sys.argv[off] == 'edit':
            edit_info()
        elif sys.argv[off] == 'upd':
            update_info()
        else:
            help_message('Info command not found')
    except IndexError:
        help_message('No info command supplied')
    
if __name__ == '__main__':
    info()