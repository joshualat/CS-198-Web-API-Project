from util import *
from lib.ConsoleTools import *
from secure_file_io import *
from help import *

def input_username(conn):
    ''' gets username from keyboard, and checks if not taken '''
    while True:
        username = ConsoleTools.accept_input('Input website username: ')
        if username:
            page = conn.secure_message('username_exists',username=username)
            if page['success']:
                return username
            else:
                pretty_print(page)
        else:
            print 'Empty username not allowed.'
            
@with_help('reg')
@verify_first
def reg_site(off=1):
    ''' registers to website '''
    conn = connect(input=True)
    try:
        conn.start()
        usb_data = usb_data_for_site()
        usb_data['username'] = input_username(conn)
        page = conn.secure_message('register', **usb_data)
        if page['success']:
            SecureFileIO.update_usb_usernames(conn.url, usb_data['username'])
        pretty_print(page)
    finally:
        if conn:
            conn.end()
    
if __name__ == "__main__":
    reg_site()
    ConsoleTools.newline(3)
    print 'Program has ended.'
    ConsoleTools.accept_input()