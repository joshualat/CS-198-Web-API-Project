from decorators import *

@usb_login_first
def login_site(off=1):
	''' logins to website '''
	#urlchoose user
	site = SecureWebConnection(url)
	#send auth
	#web open
	
if __name__ == "__main__":
	login_site()