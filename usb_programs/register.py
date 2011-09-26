from util import *
from lib.ConsoleTools import *
from secure_file_io import *
from help import *

def input_username(conn):
    ''' gets username from keyboard, and checks if not taken '''
    while True:
        username = ConsoleTools.accept_input('Input a username')
        if username:
            if not conn.secure_message('username_exists',username=username):
                return username
            print quote(username), 'is already taken'
        else:
            print 'Empty username not allowed.'
            
@with_help('reg')
@verify_first
@login_first
def reg_site(off=1):
    ''' registers to website '''
    conn = connect(input=True)
    try:
        conn.start()
        usb_data = SecureFileIO.load_usb_data()
        if usb_data.has_key('usernames'):
            usb_data.pop('usernames')
        usb_data['username'] = input_username(conn)
        page = conn.secure_message('register', **usb_data)
        if page['success']:
            SecureFileIO.update_usb_usernames(conn.url, usb_data['username'])
        print page
    finally:
        conn.end()
    
if __name__ == "__main__":
    reg_site()