# login prompt for 

import config

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

def usb_login_first(function=None):
	def _dec(func):
		def new_function(*args, **kwargs):
			if not login_usb(): return # return if login is unsuccessful
			function(*args, **kwargs)
		
        new_function.__name__ = view_func.__name__
        new_function.__dict__ = view_func.__dict__
        new_function.__doc__ = view_func.__doc__
		return new_function
	
	return _dec(function) if function else _dec
