#future: separate create usb from others

import sys
from decorators import *
from help import *
from create import *
from login import *
from logout import *
from register import *
from info import *
from change_password import *

def hello():
    print 'Hello World!'

action = {
    'create': create_usb, 
    'help': help,
    'info': info,
    'newpass': change_password,
    'reg': reg_site,
    'login': login_site,
    'logout': logout_site,
    'hello': hello,
}

if __name__ == "__main__":
    try:
        name = sys.argv[1]
        if action.has_key(name):
            action[name](off=2)
        else:
            help('Command "' + name + '" not found.');
        
    except IndexError:
        help('No command found.')
        
    ConsoleTools.newline(3)
    print 'Program has ended.'
    ConsoleTools.accept_input()
