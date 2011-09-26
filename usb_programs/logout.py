from util import *
from help import *

@with_help('logout')
@verify_first
def logout_site(off=1):
    ''' logouts from website '''
    conn = connect()
    try:
        conn.start()
        page = conn.secure_message('logout')
        pretty_print(page)
    finally:
        if conn:
            conn.end()
    
if __name__ == "__main__":
    logout_site()
    ConsoleTools.newline(3)
    print 'Program has ended.'
    ConsoleTools.accept_input()