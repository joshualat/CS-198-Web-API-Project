import os.path
from datetime import datetime
import sys
import shutil

# ConsoleTools Class

class ConsoleTools(object):

    """
    ConsoleTools class 

    Usable functions:
        accept_input
        separator
        newline
        start_timer
        end_timer
        format_usb
        read_usb
        close_usb
        plain_file_write
        file_write
        file_read

    """

    @classmethod
    def accept_input(cls,text="Press ENTER to continue...",list_of_accepted_values=None):
        if not text:
            text = ''
        if not list_of_accepted_values:#any empty sequence i also false
            user_input = raw_input(text)
        else:
            accept = False
            user_input = ""
            while not accept:
                user_input = raw_input(text+" ["+'/'.join([str(x) for x in list_of_accepted_values])+"]: ")
                accept = (user_input in list_of_accepted_values)
        return user_input

    @classmethod
    def separator(cls,length=60):
        print "-"*length

    @classmethod
    def newline(cls,n=1):
        print "\n"*(n-1)

    @classmethod
    def start_timer(cls):
        return datetime.now()

    @classmethod
    def end_timer(cls,start_time):
        secs = (datetime.now() - start_time).seconds
        if secs == 1:
            return str(secs) + " second"
        else:
            return str(secs) + " seconds"
    
    @classmethod
    def format_usb(cls,password):
        ''' Formats a usb for our use. '''
        
            
        #TODO
        #Format USB to FAT32 format
        #create truecrypt container in the target drive
        #return the path to the truecrypt container (e.g. 'D:/data/sample.mp4') if successful
        #return None (or raise exception) otherwise
        
        if sys.platform == 'win32' or sys.platform == 'cygwin':
            drive = ConsoleTools.accept_input('Enter the drive letter where USB flash drive is mounted: ')
            os.system('format %s:  /FS:FAT32' % (drive))
        else:
            os.system('sudo fdisk -l')
            drive = ConsoleTools.accept_input('Enter the USB flash drive\'s partition name: ')
            os.system('sudo umount %s' % (drive))
            os.system('sudo mkfs.vfat %s' % (drive))
            os.system('sudo mkdir /media/external')
            os.system('sudo mount -t vfat %s /media/external -o uid=1000,gid=1000,utf8,dmask=027,fmask=137' % drive)
            sample_path = 'lib/Sample.mp4'
            os.system('sudo cp %s /media/external' % (sample_path))
            os.system('truecrypt -t -c /media/external/Sample.mp4 -p %s -k "" --encryption=AES --hash=SHA-512\
                     --volume-type=hidden --size=14000000 --filesystem=FAT' % (password))
            os.system('python tcsteg.py Sample.mp4 /media/external/Sample.mp4')
            path = '/media/external/Sample.mp4'
        return path
    
    @classmethod
    def read_usb(cls,path,password):
        ''' Reads the encrypted files in usb. '''
        #TODO
        #using this password, mount the truecrypt container to a virtual disk.
        #prompt letter of virtual disk if necessary
        #return the path to the virtual disk (e.g. 'M:/') if successful
        #(end path with '/')
        #return None (or raise exception) otherwise
        
        if path == None:
            return None
        print 'Mounting usb...'
        if sys.platform == 'win32' or sys.platform == 'cygwin':
            pass
        else:
            try:
                os.system('truecrypt -m nokernelcrypto %s /media/truecrypt/' % (path))
            except:
                return None
            dir = '/media/truecrypt/'
        print 'Mount successful. Mounted to %s' % (dir)
        return dir
    
    @classmethod
    def close_usb(cls,path,diskpath,password):
        ''' Unmounts the container of the encrypted files '''
        #TODO
        #Unmount the virtual disk
        if path == None:
            return None
        print 'Unmounting usb...'
        if sys.platform == 'win32' or sys.platform == 'cygwin':
            pass
        else:
            os.system('truecrypt -d %s' % (diskpath))
        print 'Unmount successful.' # let's assume data is written properly
    
    @classmethod
    def file_write(cls,filename,text):
        ''' Writes encrypted file. '''
        target = open(filename, 'w')
        target.write(text)
        target.close()

    @classmethod
    def file_read(cls,filename):
        ''' Reads from encrypted file. '''
        if os.path.exists(filename):
            return file(filename).read()
        else:
            return None
