import os,os.path
from lib.ConsoleTools import *
from lib.PKA import *
from lib.SecTools import *

#introduction
ConsoleTools.separator()
print "Welcome to usb_api key and config generation program!"
print "Here you will be able to create or update your private key, public key, and configuration file."
ConsoleTools.separator()

#check if directory exists
if not os.path.exists("box"):
    os.makedirs('box')
    ConsoleTools.file_write('box/__init__.py',"")

#check for missing files
private_key_exists = os.path.exists("box/private.key")
public_key_exists = os.path.exists("box/public.key")
config_exists = os.path.exists("box/config")

missing_files = []
if not private_key_exists:
    missing_files.append("private.key")
if not public_key_exists:
    missing_files.append("public.key")
if not config_exists:
    missing_files.append("config")

if len(missing_files) > 0:
    print "The following file/s are missing:"
    for missing in missing_files:
        print "- %s" % missing    
    ConsoleTools.separator()

#generate or not?
user_input = ConsoleTools.accept_input("Do you wish to generate a new set of keys and configuration files?",["y","n"])
ConsoleTools.separator()

if user_input == "y":
    print "Generating new Private and Public Keys (this may take a while)..."
    start_time = ConsoleTools.start_timer()
    priv_key, pub_key = PKA.generate_keys()
    total_time = ConsoleTools.end_timer(start_time)
    print "Private and Public Keys successfully generated in " + total_time + "."
    print "Saving Private Key to 'box/private.key'..."
    ConsoleTools.file_write('box/private.key',priv_key)
    print "Saving Public Key to 'box/public.key'..."
    ConsoleTools.file_write('box/public.key',pub_key)
    print "Private and Public Key successfully saved."
    ConsoleTools.newline()
    print "Generating UUID and Salt..."
    uuid = SecTools.generate_uuid()
    salt = SecTools.generate_salt()
    print "Saving UUID and Salt to 'box/config'"
    text = uuid + "\n" + salt
    ConsoleTools.file_write('box/config',text)
    print "UUID and Salt successfully saved."
    ConsoleTools.separator()
    print "All files successfully created/updated"
    print "Ending program."
    
else:
    print "No files created. Ending program."

ConsoleTools.accept_input()
