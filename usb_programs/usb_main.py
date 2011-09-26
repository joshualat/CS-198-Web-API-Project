#future: separate create usb from others

''' 
the program's entry point.
this code must run in a valid usb account except for the 'create' command.
'''
    
import sys
from help import *
from create import *
from login import *
from logout import *
from register import *
from info import *
from change_password import *
from gen_crypt_data import *
from lib.ConsoleTools import *
import traceback

@with_help('hello')
def hello(off=1):
    ''' Prints hello world. '''
    print 'Hello World!'

def main():
    ''' the program's entry point. '''
    commands = command_info.keys()
    if len(sys.argv) <= 1:
        name = ConsoleTools.accept_input('Select command', commands)
    else:
        name = sys.argv[1]
    if command_info.has_key(name):
        try:
            command_info[name][0](off=2)
        except:
            traceback.print_exc()
    else:
        help_message('Command "' + name + '" not found.');

if __name__ == "__main__":
    main()
    ConsoleTools.newline(3)
    print 'Program has ended.'
    ConsoleTools.accept_input()
    
