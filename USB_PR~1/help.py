import sys
from lib.ConsoleTools import *

''' 
help file/information.
'''

command_info = {
    'create'    : [None, 
                    ('',          'create usb account.'),
                ],
    'info'      : [None, 
                    ('edit',      'edit user information.'),
                    ('upd[ate]',  'update user info to website/s.'),
                ],
    'reg'       : [None, 
                    ('',          'register to website.'),
                ],
    'login'     : [None, 
                    ('',          'login to website.'),
                ],
    'logout'    : [None, 
                    ('',          'logout from website.'),
                ],
    'newpass'   : [None, 
                    ('',          'replace old password with new one.'),
                ],
    'help'      : [None, 
                    ('',          'display help text.'),
                    ('<command>', 'display help text for command <command>.'),
                ],
    'hello'     : [None, 
                    ('',          'print hello world.'),
                ],
    'gen'     : [None, 
                    ('',          'generate PKA keys and hash.'),
                ],
}

def with_help(name):
    def _dec(function):
        command_info[name][0] = function
        return function
    return _dec

def quote(c):
    return "'" + c + "'"
    
def double_quote(c):
    return '"' + c + '"'

def help_command(command):
    if command_info.has_key(command):
        print 'Help for command ' + quote(command) + ':'
        ConsoleTools.newline()
        for args, info in command_info[command][1:]:
            quoted= quote(' '.join([command, args]).strip())
            print quoted, ':', info
    else:
        print 'Error: Command not found.'

def help_message(msg=''):
    ''' display help with message '''
    print 'Error:', msg
    print 'See', quote('help'), 'for help.'

@with_help('help')
def help(off=1):
    ''' displays help text '''
    if len(sys.argv) > off:
        help_command(sys.argv[off])
    else:
        print 'Possible commands:'
        print command_info.keys()
        ConsoleTools.newline()
        print 'See', quote('help <command>'), 'for more details.'

if __name__ == "__main__":
    help()
