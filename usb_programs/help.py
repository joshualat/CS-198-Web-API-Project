import sys
from lib.ConsoleTools import *

''' 
help file/information.
'''

command_info = {
    'create'    : [('',          'create usb account.')],
    'info'      : [('edit',      'edit user information.'),
                   ('update',    'update user info to website/s.')],
    'reg'       : [('',          'register to website.')],
    'info_upd'  : [('',          'register to website.')],
    'login'     : [('',          'login to website.')],
    'logout'    : [('',          'logout from website.')],
    'newpass'   : [('',          'replace old password with new one.')],
    'help'      : [('',          'display help text.'),
                   ('<command>', 'display help text for command <command>.')],
    'hello'     : [('',          'print hello world.')]
}

def quote(c):
    return '"' + c + '"'

def help_command(command):
    if command_info.has_key(command):
        print 'Help for command ' + quote(command) + ':'
        ConsoleTools.newline()
        for args, info in command_info[command]:
            quoted= quote(' '.join([command, args]).strip())
            print quoted, ':', info
    else:
        print 'Error: Command not found.'

def help_message(msg=''):
    ''' display help with message '''
    print 'Error:', msg
    print 'See', quote('help'), 'for help.'

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
