from util import *
from help import *

@with_help('logout')
@verify_first
@login_first
def logout_site(off=1):
    ''' logins to website '''
    conn = connect()
    try:
        conn.start()
        page = conn.secure_message('logout')
        print page
    finally:
        conn.end()
	
if __name__ == "__main__":
	logout_site()