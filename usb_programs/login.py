from util import *
from help import *

@with_help('login')
@verify_first
@login_first
def login_site(off=1):
    ''' logins to website '''
    conn = connect()
    try:
        conn.start()
        page = conn.secure_message('login')
        print page
    finally:
        conn.end()
    
if __name__ == "__main__":
    login_site()
