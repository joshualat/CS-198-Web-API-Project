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
    def file_write(cls,filename,text):
        target = open(filename, 'w')
        target.write(text)
        target.close()

    @classmethod
    def file_read(cls,filename):
        if os.path.exists(filename):
            return file(filename).read()
        else:
            return None
