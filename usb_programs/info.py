import sys 
from util import *
from help import *

fields = {
    'first_name': ('first name', (), True),
    'last_name': ('last name', (), True),
    'email': ('e-mail address', (), True),
    'sex': ('sex', [x[0] for x in GENDER_CHOICES], True),
    'birthdate': ('birth date', (), True),
    'address': ('address', (), False),
    'country': ('country', (), False),
    'contact_number': ('contact number', (), False),
}
    
@verify_first
def edit_info(path=''):
    '''
        edits user information stored on usb drive 
    '''
    usb_data = SecureFileIO.load_usb_data(path=path)
    def input_name(name,choices):
        text = 'Input ' + name
        if not choices:
            text += ': '
        return ConsoleTools.accept_input(text, choices).strip()
    
    for field, field_tuple in fields.items():
        name, choices, required = field_tuple
        has_name = usb_data.has_key(name) and usb_data['name']
        if has_name:
            print 'Current', name + ':', usb_data['name'],
        else:
            print 'No', name, 'yet.',
        if required: 
            name += '*'
        if required and not has_name:
            value = input_name(name,choices)
            while not value:
                print 'Required field cannot be left blank.'
                value = input_name(name,choices)
        elif ConsoleTools.accept_input('Change?', ['y','n']) == 'y':
            value = input_name(name,choices)
            if required and not value:
                print 'Required field cannot be left blank. No change done.'
                value = None
        if not required or value != None:
            usb_data[field] = value
    SecureFileIO.save_usb_data(usb_data,path=path)
    print 'Edit info successful!'


@verify_first
def update_info(target_conn=None):
    '''updates user information stored to website '''
    if not target_conn:
        target_conn=connect()
    user_info = SecureFileIO.load_usb_data()
    page = target_conn.secure_message('edit_user_info', **user_info)
    pretty_print(page)
    
@with_help('info')
def info(path='',off=1):
    ''' update information in usb or to website '''
    if off >= len(sys.argv):
        command = ConsoleTools.accept_input('Select command', ['edit', 'upd', 'update'])
    else:
        command = sys.argv[off]
    if command == 'edit':
        edit_info(path=path)
    elif command in ['upd', 'update']:
        update_info()
    else:
        help_message('Info command not found.')
    
if __name__ == '__main__':
    info()
    ConsoleTools.newline(3)
    print 'Program has ended.'
    ConsoleTools.accept_input()