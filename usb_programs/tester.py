from secure_web_connection import *
swc = SecureWebConnection("http://localhost:8000/")
swc.exchange_keys()
swc.generate_shared_key()
swc.transfer_shared_key()
swc.delete_shared_key()
