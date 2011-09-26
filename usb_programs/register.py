from util import *
from secure_file_io import *

def input_username(conn):
    ''' gets username from keyboard, and checks if not taken '''
    while True:
        username = conn.accept_input('Input a username:')
        if username:
            if not conn.secure_message('username_exists',username=username):
                return username
            print quote(username), 'is already taken'
        else:
            print 'Empty username not allowed.'

@login_first
def reg_site(off=1):
    ''' registers to website '''
    conn = connect()
    try:
        conn.start()
        usb_data = SecureFileIO.load_usb_data()
        usb_data = input_username(conn)
        page = conn.secure_message('register', **usb_data)
    finally:
        conn.end()
    print page
    
if __name__ == "__main__":
    reg_site()