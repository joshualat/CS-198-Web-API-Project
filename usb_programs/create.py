from lib.ConsoleTools import *
from help import *
from util import *
from gen_crypt_data import *
import shutil
from info import *

@with_help('create')
def create_usb(off=1):
    ''' 
    creates usb account: formats usb drive, registers it to main site, and gathers data. 
    this code may be run anywhere.
    '''
    
    confirm = ConsoleTools.accept_input('WARNING: ALL data from USB will be deleted. Continue?',['y','n'])
    if confirm == 'y':
        password = input_password()
        print 'pass =', password
        set_password(password)
        
        print 'Formatting usb...'
        path=ConsoleTools.format_usb(password)
        print 'Opening usb...'
        diskpath=ConsoleTools.read_usb(path,password)
        if not (path and diskpath):
            raise Error()
        try:
            diskpath += 'crypt_data/'
            print 'Copying files to', diskpath, '...'
            shutil.copytree('.', diskpath)
            os.makedirs(diskpath + 'box')
            gen_crypt_data(path=diskpath)
            print 'Editing information...'
            edit_info(path=diskpath)
            print 'New USB account successfully created.'
        finally:
            ConsoleTools.close_usb(path,diskpath,password)
    else:
        print 'No files created.'
    
if __name__ == "__main__":
    create_usb()
