import os.path
from datetime import datetime

# ConsoleTools Class

class ConsoleTools(object):

    """
    ConsoleTools class 

    Usable functions:
        accept_input

    """

    @classmethod
    def accept_input(cls,text="Press ENTER to continue...",list_of_accepted_values=None):
        if list_of_accepted_values == None or list_of_accepted_values == []:
            user_input = raw_input(text)
        else:
            accept = False
            user_input = ""
            while accept!=True:
                user_input = raw_input(text+" ["+'/'.join([str(x) for x in list_of_accepted_values])+"]: ")
                if user_input in list_of_accepted_values:
                    accept = True
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
        #Formats USB to FAT32 format
        if sys.platform == 'win32' or sys.platform == 'cygwin':
            drive = ConsoleTools.accept_input('Enter the drive letter where USB flash drive is mounted: ')
            os.system('format %s:  /FS:FAT32' % (drive))
        else:
            print 'Please identify the USB flash drive\'s partition name.'
            os.system('sudo fdisk -l')
            drive = ConsoleTools.accept_input('Enter the USB flash drive\'s partition name: ')
            os.system('sudo umount %s' % (drive))
            os.system('sudo mkfs.vfat %s' % (drive))
            
        #create truecrypt container in the target drive
        #call read_usb with this password
        #return True if successful, False (or exception) otherwise
        return True
    
    @classmethod
    def read_usb(cls,password):
        ''' Reads the encrypted files in usb. '''
        #using this password, mount the truecrypt container to a virtual disk.
        #return True if successful, False (or exception) otherwise
        return True

    @classmethod
    def close_usb(cls,password):
        #Unmount the virtual disk
        pass
    
    @classmethod
    def plain_file_write(cls,filename,text):
        ''' Writes to file. '''
        #write text into filename in the target drive WITHOUT encryption, i.e., plain write.
        #note that it must be written in the target drive, NOT the virtual disk.
        target = open(filename, 'w')
        target.write(text)
        target.close()
        
    @classmethod
    def file_write(cls,filename,text):
        ''' Writes encrypted file. '''
        #write text into filename in the virtual disk WITH encryption.
        #note that it must be written in the virtual disk, NOT the target drive.
        target = open(filename, 'w')
        target.write(text)
        target.close()

    @classmethod
    def file_read(cls,filename):
        ''' Reads from encrypted file. '''
        #read text from filename in the virtual disk WITH encryption.
        #note that it must be read from the virtual disk, NOT the target drive.
        if os.path.exists(filename):
            return file(filename).read()
        else:
            return None
