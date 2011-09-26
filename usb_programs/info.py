import sys 
from util import *
from help import *


fields = {
    'first_name': ('first name', ()),
    'last_name': ('last name', ()),
    'email': ('e-mail address', ()),
    'sex': ('sex', GENDER_CHOICES),
    'birthdate': ('birth date', ()),
    'address': ('address', ()),
    'country': ('country', ()),
    'contact_number': ('contact number', ()),
}

'''
'''
    
@verify_first
@login_first
def edit_info(path=''):
    '''
        edits user information stored on usb drive 
        
        For simplicity, all data will be optional
        FROM TESTSITE:
        
        #required fields
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
    usb_data = SecureFileIO.load_usb_data(path=path)
    for field, name, choices in fields.items():
        value = ConsoleTools.accept_input('Input ' + name + ' (leave blank for no change)', choices)
        if value:
            usb_data[field] = value
    SecureFileIO.save_usb_data(usb_data,path=path)

@verify_first
@login_first
def update_info(target_conn=None):
    '''updates user information stored to website '''
    if not target_conn:
        target_conn=connect()
    user_info = SecureFileIO.load_usb_data()
    page = target_conn.secure_message('edit_user_info', **user_info)
    print page
    
@with_help('info')
def info(path='',off=1):
    try:
        if sys.argv[off] == 'edit':
            edit_info(path=path)
        elif sys.argv[off] == 'upd':
            update_info()
        else:
            help_message('Info command not found')
    except IndexError:
        help_message('No info command supplied')
    
if __name__ == '__main__':
    info()