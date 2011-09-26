from util import *

@login_first
def logout_site(off=1):
    ''' logins to website '''
    conn = connect()
    try:
        conn.start()
        page = conn.secure_message('logout')
    finally:
        conn.end()
    print page
	
if __name__ == "__main__":
	logout_site()