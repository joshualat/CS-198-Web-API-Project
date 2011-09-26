from util import *
from help import *

@with_help('login')
@verify_first
def login_site(off=1):
    ''' logins to website '''
    conn = connect()
    try:
        conn.start()
        page = conn.secure_message('login')
        pretty_print(page)
    finally:
        if conn:
            conn.end()
    
if __name__ == "__main__":
    login_site()
    ConsoleTools.newline(3)
    print 'Program has ended.'
    ConsoleTools.accept_input()
