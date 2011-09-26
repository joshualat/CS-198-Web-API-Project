from util import *

@login_first
def login_site(off=1):
    ''' logins to website '''
    conn = connect()
    try:
        conn.start()
        page = conn.secure_message('login')
    finally:
        conn.end()
    print page
    
if __name__ == "__main__":
    login_site()
