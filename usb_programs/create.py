from ConsoleTools import *

def create_usb():
	''' creates usb account: formats usb drive, registers it to main site, and gathers data. '''
	
	confirm = ConsoleTools.accept_input('WARNING: ALL data from USB will be deleted. Continue?',['y','n'])
	if confirm == 'y':
		password = input_password()
        
        ConsoleTools.format_usb(password)
        
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
		
        #write programs to usb
		edit_info()

if __name__ == "__main__":
	create_usb()
