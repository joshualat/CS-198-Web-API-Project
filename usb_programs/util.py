from lib.ConsoleTools import *

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

password = None
MAIN_SITE = 'http://localhost:8000/'
path = ''#replace with path to drive (end it with /)

def login_usb():
	'''gathers password for reading of usb data'''
	if config.password: return True
	message = 'Enter USB password: '
	for i in range(1, ATTEMPTS + 1):
		config.password = getpass(message)
		#validate password. set to None if bad.
		if config.password: return True
		message = 'Try again. Enter USB password: '
	print 'No more attempts.'
	return False

def input_password(msg = 'Enter password'):
	'''gets new password from user two times.'''
	while True:
		pass1 = getpass(msg + ': ')
		pass2 = getpass(msg + ' (again): ')
		if len(pass1) == 0 or len(pass2) == 0:
			print "Please input the password twice."
			continue
		if pass1 == pass2: return pass1
		print "Passwords didn't match."