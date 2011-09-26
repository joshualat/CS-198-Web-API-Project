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
        set_password(password)
        
        path=ConsoleTools.format_usb(password)
        diskpath=ConsoleTools.read_usb(path,password)
        if not (path and diskpath):
            raise Exception()
        try:
            cryptpath = diskpath + 'crypt_data/'
            print 'Copying files to', cryptpath, '...'
            shutil.copytree('.', cryptpath)
            os.makedirs(cryptpath + 'box')
            print
            gen_crypt_data(path=cryptpath)
            print 'Hashing password...'
            hashed = SecTools.generate_hash(password,SecureWebConnection.usb_salt(cryptpath))
            print "Saving Public Key to", quote(cryptpath + "box/hashedpass") + "..."
            ConsoleTools.file_write(cryptpath + 'box/hashedpass',hashed)
            try:
                print
                print 'Editing information...'
                edit_info(path=cryptpath)
            except:
                traceback.print_exc()
            print
            print 'New USB account successfully created.'
        finally:
            print
            ConsoleTools.close_usb(path,diskpath,password)
    else:
        print 'Nothing done.'
    
if __name__ == "__main__":
    create_usb()
    ConsoleTools.newline(3)
    print 'Program has ended.'
    ConsoleTools.accept_input()
