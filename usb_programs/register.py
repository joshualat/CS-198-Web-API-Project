from util import *
from secure_file_io import *

@login_first
def reg_site(off=1):
	''' registers to website '''
	#urlinp user
    #call update info
    conn = SecureWebConnection(url_input(), hashed_password())
    conn.start()
    usb_data = SecureFileIO.load_usb_data()
    page = conn.secure_message('register', **usb_data)
    conn.end()
    print page
	
if __name__ == "__main__":
	register()