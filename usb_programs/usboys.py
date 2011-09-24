# usboys.py, for lack of better name at the moment

#future: separate create usb from others

import sys
from lib.ConsoleTools import *
from lib.PKA import *
from lib.SKA import *
from secure_web_connection import *
from getpass import getpass

MAIN_SITE = 'joshua.lat'
ATTEMPTS = 3
path = ''#replace with path to drive (end it with /)

def command(c):
	return 'usboys.py ' + c

def quote_command(c):
	return '"' + command(c) + '"'

command_info = {
	'create' : [('',          'create usb account')],
	'edit'   : [('info',      'edit user information'),
			    ('password',  'edit usb password')],
	'reg'    : [('',          'register to website')],
	'login'  : [('',          'login to website')],
	'help'   : [('',          'display help text'),
			    ('<command>', 'display help text for command <command>')],
}

def help_command(command):
	if command_info.has_key(command):
		for args, info in command_info[command]:
			quoted_command = quote_command(' '.join([command, args]).strip())
			print quoted_command, info
	else:
		print 'Error: Command not found.'

def help(msg=None):
	if msg:
		print 'Error:', msg
		print 'See', quote_command('help'), 'for help'
	elif len(sys.argv) <= 2:
		print 'Possible commands:'
		for x in ['create', 'edit', 'reg', 'login', 'help']:
			print command(x)
		print 'See', quote_command('help <command>'), 'for more details'
	else:
		help_command(sys.argv[2])

password = None

def usb_login_needed(function):
	def new_function(*args, **kwargs):
		#require existence
		if not login_usb(): return
		function(*args, **kwargs)
	return new_function

def login_usb():
	'''gathers password for reading of usb data'''
	global password
	if password: return True
	message = 'Enter USB password: '
	for i in range(1, ATTEMPTS + 1):
		password = getpass(message)
		#validate password. set to None if bad.
		if password: return True
		message = 'Try again. Enter USB password: '
	print 'No more attempts.'
	return False

@usb_login_needed
def edit_info():
	'''edits user information stored on usb drive (and perhaps website) '''
	#get data from disk
	#edit all fields
	#if field is optional, ask if edit is wanted (or make a mechanism on how to leave it unchanged)
	#save data to disk
	pass

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

@usb_login_needed
def edit_password():
	'''edits usb password'''
	new_pass = input_password()
	#change usb password.
	pass


def edit():
	if len(sys.argv) > 2:
		if sys.argv[2] == 'info':
			edit_info()
			return
		elif sys.argv[2] == 'password':
			edit_password()
			return
	print 'Edit command not found'
	help_command('edit')

def format_usb():
	global password
	''' formats usb for usage. '''
	confirm = ConsoleTools.accept_input('WARNING: ALL data from USB will be deleted. Continue?',['y','n'])
	if confirm == 'y':
		password = input_password()
		#format usb with password
		return True
	return False

def create_usb():
	''' creates usb account: formats usb drive, registers it to main site, and gathers data. '''
	if not format_usb(): return
    print "Generating new Private and Public Keys (this may take a while)..."
    start_time = ConsoleTools.start_timer()
    priv_key, pub_key = PKA.generate_keys()
    total_time = ConsoleTools.end_timer(start_time)
    print "Private and Public Keys successfully generated in " + total_time + "."
    print "Saving Private Key to 'box/private.key'..."
    ConsoleTools.file_write(path + 'box/private.key',priv_key)
    print "Saving Public Key to 'box/public.key'..."
    ConsoleTools.file_write(path + 'box/public.key',pub_key)
    print "Private and Public Key successfully saved."
    ConsoleTools.newline()
    print "Generating UUID and Salt..."
    uuid = SecTools.generate_uuid()
    salt = SecTools.generate_salt()
    print "Saving UUID and Salt to 'box/config'"
    text = uuid + "\n" + salt
    ConsoleTools.file_write(path + 'box/config',text)
    print "UUID and Salt successfully saved."
	#register to website
	#write programs to usb
	edit_info()


@usb_login_needed
def reg_site(url):
	''' registers to website '''
	input_website
	#get urldata
	#save urldata

@usb_login_needed
def reg_site():
	''' registers to website '''
	#urlinp user
	pass

@usb_login_needed
def login_site():
	''' logins to website '''
	#urlchoose user
	site = SecureWebConnection(url)
	#send auth
	#web open

if __name__ == "__main__":
	if len(sys.argv) <= 1:
		help('No command found.')
	elif sys.argv[1] == 'help':
		help()
	elif sys.argv[1] == 'create':
		create_usb()
	elif sys.argv[1] == 'edit':
		edit()
	elif sys.argv[1] == 'reg':
		reg_site()
	elif sys.argv[1] == 'login':
		login_site()
	else:
		help('Command "' + sys.argv[1] + '" not found.');

	ConsoleTools.newline()
	print 'Program has ended.'
	ConsoleTools.accept_input()
