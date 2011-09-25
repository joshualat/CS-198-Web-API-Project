from decorators import *

@usb_login_first
def logout_site(off=1):
	''' logins to website '''
	#urlchoose user
	site = SecureWebConnection(url)
	#send auth
	
if __name__ == "__main__":
	logout_site()