from util import *
from secure_web_connection import *

@login_first
def login_site(off=1):
    ''' logins to website '''
    conn = SecureWebConnection(url_choose(), hashed_password())
    conn.start()
    page = conn.secure_message('login')
    conn.end()
    print page
    
if __name__ == "__main__":
    login_site()
